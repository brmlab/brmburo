import re
import datetime
import logging

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from brmburo.models import LogicTransaction, LogicTransactionSplit, LogicAccount, LogicAccountType, SecurityPrincipal, \
    Buddy, BuddyType, BuddyEvent, BuddyEventType, BankTransaction, Currency
from brmburo.transactions import account_sum
from .helpers import view_POST, view_GET, combine
from .forms import LoginForm, AddBuddyForm, BuddyAdminForm

logger = logging.getLogger(__name__)


@view_POST(
    r'^login/do$',
    form_cls = {'login':LoginForm,},
    invalid_form_msg = 'Login form invalid.',
    redirect_to = '/',
    redirect_attr = 'next',
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
    next = combine(request.GET, request.POST).get('next', '/')
    if request.user and request.user.is_authenticated():
        return redirect(next)
    return {
        'next': next
    }

@view_GET(
    r'^logout$',
    redirect_to = '/',
    redirect_attr = 'next',
    decorators = ( cache.never_cache,  ),
)
def logout(request, forms):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'User deauthentication successful.')

@view_GET( r'^roster$', template = 'roster.html')
@login_required
def roster(request, **kw):
    from models import Buddy

    # only superuser can view full roster (it contains balances etc.)
    # redirect user if his username matches logged in user (authorization for roster detail is done in that view)
    if not request.user.is_superuser:
        try:
            buddy = Buddy.objects.get(nickname__iexact=request.user.username)
            return redirect("roster_user", uid=buddy.uid)
        except Buddy.DoesNotExist:
            return {
                'authorized': False,
            }

    return {
        'authorized': True,
        'users':
            ((buddy,account_sum(buddy)) for buddy in Buddy.objects.all().order_by('nickname')),
    }

@view_GET( r'^account/list$', template = 'account_list.html')
@login_required
def account_list(request, **kw):
    def getbuddy(account):
        buddy = Buddy.objects.filter(logic_account=account)
        return buddy[0] if buddy.exists() else None

    # only superuser can view all accounts (they contain balances etc.)
    if not request.user.is_superuser:
        return {
            'authorized': False,
        }

    return {
        'authorized': True,
        'accounts': ( (account,account_sum(account),getbuddy(account)) for account in  LogicAccount.objects.all() ),
        }

@view_GET( r'^transaction/list$', template = 'transaction_list.html')
@login_required
def transaction_list(request, **kw):
    # only superuser can view all transactions
    if not request.user.is_superuser:
        return {
            'authorized': False,
            }

    transactions = LogicTransaction.objects.all()
    bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=False)
    ignored_bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=True)

    paginator = Paginator(transactions, 25) # Show 25 transactions per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)

    return {
        'authorized': True,
        'transactions': results,
        'counts': {
            'transactions': transactions.count(),
            'bank_transactions': bank_transactions.count(),
            'ignored_bank_transactions': ignored_bank_transactions.count(),
            }
        }

@view_GET( r'^bank-transaction/list/(?P<category>ignored|new)$', template='bank_transaction_list.html')
@login_required
def bank_transaction_list(request, category, **kw):
    # only superuser can view all transactions
    if not request.user.is_superuser:
        return {
            'authorized': False,
            }

    transactions = LogicTransaction.objects.all()
    bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=False)
    ignored_bank_transactions = BankTransaction.objects.filter(logic_transaction__isnull=True, ignored=True)

    paginator = Paginator(ignored_bank_transactions if category == 'ignored' else bank_transactions, 25) # Show 25 transactions per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)

    return {
        'authorized': True,
        'transactions':  results,
        'ignored': category == 'ignored',
        'counts': {
            'transactions': transactions.count(),
            'bank_transactions': bank_transactions.count(),
            'ignored_bank_transactions': ignored_bank_transactions.count(),
            }
        }

@view_POST(r'^bank-transaction/detail/ignore$',
           form_cls=None,
           redirect_to=None,
           redirect_attr='nexturl',
           decorators=(cache.never_cache,)
)
@login_required
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
        return {
            'no_such_uid': True,
            'authorized': False,
            'uid': uid,
        }

    # Old way - look at user is set in buddy's settings
    # allow only superuser if buddy has no 'user' field set that would allow anyone to view it
    # allow only user specified in admin or superuser if 'user' is specified
    #if not request.user.is_superuser and buddy.nickname.lower() != request.user.username.lower():

    # Less secure way - do not look at buddy's settings, show roster detail if login name and buddy name match
    if not request.user.is_superuser and (not buddy.user or buddy.user.username != request.user.username):
        return {
            'authorized': False,
            'buddy': buddy,
        }

    history = []

    for event in BuddyEvent.objects.filter(buddy=buddy).order_by('date'):
        history.append(dict(date=event.date,type=event.type.name,reason=event.reason,color='success'))
        if event.until:
            history.append(dict(date=event.until,type=event.type.name,reason='END of %s %s' % (event.type.name, event.reason),color='error'))

    for split in LogicTransactionSplit.objects.filter(account=buddy.logic_account):
        history.append(dict(
            date=split.transaction.time.date(),
            type='debit' if split.side < 0 else 'credit',
            amount=split.amount_,
            currency=split.account.currency.symbol,
            reason=split.transaction.comment,
            color='warning' if split.side < 0 else 'info'
        ))

    return {
        'authorized': True,
        'buddy': buddy,
        'balance': account_sum(buddy),
        'events': BuddyEvent.objects.filter(buddy=buddy).order_by('date'),
        'history': sorted(history, key=lambda h: h.get('date')),
        'principals': SecurityPrincipal.objects.filter(buddy=buddy).order_by('since'),
        'can_edit': request.user.is_superuser,
        }

@view_GET( r'^account/detail/(?P<id>[0-9]*)$', template = 'account_detail.html')
@login_required
def account_detail(request, id, **kw):
    # only superuser can view account details - it could be more finegrained, but it's like this for now
    if not request.user.is_superuser:
        return {
            'authorized': False,
        }

    account = LogicAccount.objects.get(id=int(id))
    buddy = Buddy.objects.filter(logic_account=account)
    return {
        'authorized': True,
        'account': account,
        'buddy': buddy[0] if buddy.exists() else None,
        'balance': account_sum(account),
        'splits': LogicTransactionSplit.objects.filter(account=account).order_by('transaction__time'),
        }


@view_GET( r'^transaction/detail/(?P<id>[0-9]*)$', template = 'transaction_detail.html')
@login_required
def transaction_detail(request, id, **kw):
    # only superuser can view transaction details - it could be more finegrained, but it's like this for now
    if not request.user.is_superuser:
        return {
            'authorized': False,
            }
    transaction = LogicTransaction.objects.get(id=id)
    return {
        'authorized': True,
        'transaction': transaction,
        'splits': LogicTransactionSplit.objects.filter(transaction=transaction)
    }

@view_GET( r'^bank-transaction/detail/(?P<id>[0-9]*)$', template = 'bank_transaction_detail.html')
@login_required
def bank_transaction_detail(request, id, **kw):
    # only superuser can view transaction details - it could be more finegrained, but it's like this for now
    if not request.user.is_superuser:
        return {
            'authorized': False,
            }
    transaction = BankTransaction.objects.get(id=id)
    return {
        'authorized': True,
        'transaction': transaction,
    }

@view_GET( r'^buddy/add/$', template = 'buddy_add.html', decorators = ( cache.never_cache,  ),)
@login_required
def buddy_add(request, **kw):
    if not request.user.is_superuser:
        return {
            'authorized': False,
        }

    form = AddBuddyForm({"uid": BuddyAdminForm.get_default_prime()})

    return {
        'form': form,
        'authorized': 'True'}

@view_POST(r'^buddy/add/new/$',
           form_cls=None,
           redirect_to="/",
           redirect_attr='nexturl',
           decorators=(cache.never_cache,)
           )
@login_required
def buddy_add_new(request, forms, **kw):
    if not request.user.is_superuser:
        return

    form = AddBuddyForm(request.POST.copy())

    # make just year also accepted in "born" field
    m = re.match(r"^\d{4}$", form.data["born"])
    if m:
        form.data["born"] = m.group(0) + "-01-01"

    if not form.is_valid():
        messages.error(request, 'Buddy addition was rejected because form was invalid. Required are: UID, nick, buddy type.')
        return

    buddy = form.save(commit=False)
    # automatically create logic account and start buddy event for member
    # this will raise exception if buddy type with symbol "member" or buddy event type "start" does not exist yet
    if buddy.type == BuddyType.objects.get(symbol="member"):
        logic_account = LogicAccount.objects.create(
            name = "Payments from %s %s" % (buddy.first_name, buddy.surname),
            symbol = "@%s" % buddy.nickname,
            currency = Currency.objects.get(symbol="CZK"),
            type = LogicAccountType.objects.get(symbol="credit")
        )
        buddy.logic_account = logic_account
    buddy.save()
    event_type = BuddyEventType.objects.get(symbol="start")
    event = BuddyEvent.objects.create(
        buddy=buddy,
        type=event_type,
        date=datetime.date.today(),
        reason="Buddy %s created" % buddy.nickname,
    )
    messages.success(request, 'Buddy addition was successful.')
