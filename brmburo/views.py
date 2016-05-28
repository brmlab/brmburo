import re
import logging

from django.contrib import messages
from django.views.decorators import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME

from brmburo.models import LogicTransaction, LogicTransactionSplit, LogicAccount, SecurityPrincipal, Buddy, BuddyEvent, BankTransaction, BuddyType, LogicAccountType, BuddyEventType, PrincipalType
from .transactions import account_sum
from .buddies import buddy_for_logic_account, after_create_buddy
from .helpers import view_POST, view_GET, combine, NotAuthorizedException, superuser_required, paginate
from .forms import LoginForm, BuddyForm


logger = logging.getLogger(__name__)


@view_POST(
    r'^login/do$',
    form_cls = {'login':LoginForm,},
    invalid_form_msg = 'Login form invalid.',
    redirect_to = '/',
    redirect_attr = REDIRECT_FIELD_NAME,
    decorators = ( cache.never_cache,  ),
)
def do_login(request, forms):
    from django.contrib.auth import login,authenticate
    form = forms['login']
    try:
        if form.is_valid():
            user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'User authentication was successful.')
                    return
                else:
                    messages.error(request, 'User account has been disabled.')
                    return
    except Exception:
        pass
    messages.error(request, 'User authentication was unsuccessful.')


@view_GET(
    r'^login$',
    template = 'login.html',
    decorators = ( cache.never_cache,  ),
)
def login(request, forms):
    next = combine(request.GET, request.POST).get(REDIRECT_FIELD_NAME, '/')
    if request.user and request.user.is_authenticated():
        return redirect(next)
    return {
        'next': next
    }


@view_GET(
    r'^logout$',
    redirect_to = '/',
    redirect_attr = REDIRECT_FIELD_NAME,
    decorators = ( cache.never_cache,  ),
)
def logout(request, forms):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'User deauthentication successful.')


@view_GET( r'^roster$', template = 'roster.html')
@login_required
def roster(request, **kw):
    type = request.GET.get('type')
    try:
        BuddyType.objects.get(symbol=type)
    except BuddyType.DoesNotExist:
        type = 'member'

    # only superuser can view full roster (it contains balances etc.)
    # redirect user if his username matches logged in user (authorization for roster detail is done in that view)
    if not request.user.is_superuser:
        try:
            buddy = Buddy.objects.get(user=request.user)
            return redirect("roster_user", uid=buddy.uid)
        except Buddy.DoesNotExist:
            raise NotAuthorizedException('Superuser required.')

    types = {}
    for t in BuddyType.objects.all():
        types[t.symbol] = (t,Buddy.objects.filter(type=t).count())

    return {
        'users': paginate(
            Buddy.objects.filter(type__symbol=type).order_by('nickname'),
            request.GET.get('page'),
            lambda buddy: (buddy,account_sum(buddy))
        ),
        'type': type,
        'types': types,
    }


@view_GET( r'^account/list$', template = 'account_list.html')
@login_required
@superuser_required
def account_list(request, **kw):
    type = request.GET.get('type')
    try:
        LogicAccountType.objects.get(symbol=type)
    except LogicAccountType.DoesNotExist:
        type = 'credit'

    types = {}
    for t in LogicAccountType.objects.all():
        types[t.symbol] = (t,LogicAccount.objects.filter(type=t).count())

    return {
        'accounts': paginate(
            LogicAccount.objects.filter(type__symbol=type),
            request.GET.get('page'),
            lambda account: (account,account_sum(account),buddy_for_logic_account(account))
        ),
        'type': type,
        'types': types,
    }


@view_GET( r'^transaction/list$', template = 'transaction_list.html')
@login_required
@superuser_required
def transaction_list(request, **kw):

    transactions = LogicTransaction.objects.all()
    bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=False)
    ignored_bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=True)

    return {
        'transactions': paginate(transactions, request.GET.get('page')),
        'counts': {
            'transactions': transactions.count(),
            'bank_transactions': bank_transactions.count(),
            'ignored_bank_transactions': ignored_bank_transactions.count(),
            }
        }


@view_GET( r'^bank-transaction/list/(?P<category>ignored|new)$', template='bank_transaction_list.html')
@login_required
@superuser_required
def bank_transaction_list(request, category, **kw):

    transactions = LogicTransaction.objects.all()
    bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=False)
    ignored_bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=True)

    return {
        'transactions':  paginate(
            ignored_bank_transactions if category == 'ignored' else bank_transactions,
            request.GET.get('page')
        ),
        'ignored': category == 'ignored',
        'counts': {
            'transactions': transactions.count(),
            'bank_transactions': bank_transactions.count(),
            'ignored_bank_transactions': ignored_bank_transactions.count(),
            }
    }


@view_POST(
    r'^bank-transaction/detail/ignore$',
    form_cls=None,
    redirect_to=None,
    redirect_attr='nexturl',
    decorators=(cache.never_cache,)
)
@login_required
@superuser_required
def bank_transaction_ignore(request, forms, **kw):
    transaction = BankTransaction.objects.get(id=int(request.POST['id']))
    transaction.ignored = not transaction.ignored
    transaction.save()
    if transaction.ignored:
        messages.success(request, 'Transaction #%s moved to ignore list.' % transaction.id)
    else:
        messages.success(request, 'Transaction #%s moved from ignore list.' % transaction.id)


@view_GET( r'^roster/user/(?P<uid>[0-9]*)$', template = 'roster_user.html')
@login_required
def roster_user(request, uid, **kw):
    try:
        buddy = Buddy.objects.get(uid=int(uid))
    except Buddy.DoesNotExist:
        if not request.user.is_superuser:
            raise NotAuthorizedException('Superuser required.')
        return {
            'no_such_uid': True,
            'uid': uid,
            }

    if not request.user.is_superuser and (not buddy.user or buddy.user != request.user):
        raise NotAuthorizedException('Superuser or %s required.' % buddy.username)

    history = []

    for event in BuddyEvent.objects.filter(buddy=buddy).order_by('date'):
        history.append(dict(
            date=event.date,
            type=event.type.name,
            reason=event.reason,
            color='success',
            id=event.id,
            target='',
        ))
        if event.until:
            history.append(dict(
                date=event.until,
                type=event.type.name,
                reason='END of %s %s' % (event.type.name, event.reason),
                color='error',
                target='',
            ))

    for split in LogicTransactionSplit.objects.filter(account=buddy.logic_account):
        history.append(dict(
            date=split.transaction.time.date(),
            type='debit' if split.side < 0 else 'credit',
            amount=split.amount_,
            currency=split.account.currency.symbol,
            reason=split.transaction.comment,
            color='warning' if split.side < 0 else 'info',
            id=split.transaction.id,
            target='transaction_detail',
        ))

    return {
        'buddy': buddy,
        'balance': account_sum(buddy),
        'events': BuddyEvent.objects.filter(buddy=buddy).order_by('date'),
        'history': sorted(history, key=lambda h: h.get('date')),
        'principals': SecurityPrincipal.objects.filter(buddy=buddy).order_by('since'),
        'can_edit': request.user.is_superuser,
        'event_types': BuddyEventType.objects.all().order_by('name'),
        'principal_types': PrincipalType.objects.all().order_by('name'),
        }


@view_GET( r'^account/detail/(?P<id>[0-9]*)$', template = 'account_detail.html')
@login_required
@superuser_required
def account_detail(request, id, **kw):

    account = LogicAccount.objects.get(id=int(id))
    buddy = Buddy.objects.filter(logic_account=account)
    return {
        'account': account,
        'buddy': buddy[0] if buddy.exists() else None,
        'balance': account_sum(account),
        'splits': LogicTransactionSplit.objects.filter(account=account).order_by('transaction__time'),
        }


@view_GET( r'^transaction/detail/(?P<id>[0-9]*)$', template = 'transaction_detail.html')
@login_required
@superuser_required
def transaction_detail(request, id, **kw):

    transaction = LogicTransaction.objects.get(id=id)
    try:
        bank_transaction = BankTransaction.objects.get(logic_transaction=transaction)
    except BankTransaction.DoesNotExist:
        bank_transaction = None

    return {
        'transaction': transaction,
        'bank_transaction': bank_transaction,
        'splits': LogicTransactionSplit.objects.filter(transaction=transaction)
    }


@view_GET( r'^bank-transaction/detail/(?P<id>[0-9]*)$', template = 'bank_transaction_detail.html')
@login_required
@superuser_required
def bank_transaction_detail(request, id, **kw):

    transaction = BankTransaction.objects.get(id=id)
    return {
        'transaction': transaction,
    }



@view_GET(
    r'^buddy/add/$',
    template = 'buddy_add.html',
    decorators = ( cache.never_cache,  ),
    form_cls = {'add_buddy':BuddyForm,},
    )
@login_required
@superuser_required
def buddy_add(request, **kw):

    return {}


@view_POST(
    r'^buddy/add/new/$',
    form_cls={'add_buddy':BuddyForm,},
    invalid_form_msg='Buddy addition was rejected because form was invalid.',
    template = 'buddy_add.html',
    decorators=(cache.never_cache,)
)
@login_required
@superuser_required
def buddy_add_new(request, forms, **kw):

    form = forms['add_buddy']

    # make just year also accepted in "born" field
    m = re.match(r"^\d{4}$", form.data["born"])
    if m:
        form.data["born"] = m.group(0) + "-01-01"

    if not form.is_valid():
        return
    
    buddy = form.save(commit=False)
    # automatically create logic account and start buddy event for member

    after_create_buddy(buddy)

