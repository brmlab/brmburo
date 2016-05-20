from brmburo.models import LogicTransaction, LogicTransactionSplit, LogicAccount, BuddyEvent, SecurityPrincipal, Buddy
from brmburo.transactions import account_sum

__author__ = 'pborky'

from django.contrib import messages
from django.views.decorators import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .helpers import view_POST, view_GET, combine
from .forms import LoginForm


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

    return {
        'authorized': True,
        'transactions': ((transaction,LogicTransactionSplit.objects.filter(transaction=transaction).count()) for transaction in LogicTransaction.objects.all().order_by('time') ),
        }

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