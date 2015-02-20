from brmburo.models import LogicTransaction, LogicTransactionSplit, LogicAccount, BuddyEvent, SecurityPrincipal, Buddy
from brmburo.transactions import account_sum

__author__ = 'pborky'

from django.contrib import messages
from django.views.decorators import cache
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
def roster(request, **kw):
    from models import Buddy

    return {
        'users':
            ((buddy,account_sum(buddy)) for buddy in Buddy.objects.all().order_by('nickname')),
    }

@view_GET( r'^account/list$', template = 'account_list.html')
def account_list(request, **kw):
    from models import LogicAccount

    return {
        'accounts': ( (account,account_sum(account)) for account in  LogicAccount.objects.all() ),
        }

@view_GET( r'^transaction/list$', template = 'transaction_list.html')
def transaction_list(request, **kw):
    return {
        'transactions': ((transaction,LogicTransactionSplit.objects.filter(transaction=transaction).count()) for transaction in LogicTransaction.objects.all().order_by('time') ),
        }

@view_GET( r'^roster/user/(?P<uid>[0-9]*)$', template = 'roster_user.html')
def roster_user(request, uid, **kw):
    buddy = Buddy.objects.get(uid=int(uid))
    return {
        'user': buddy,
        'balance': account_sum(buddy),
        'events': BuddyEvent.objects.filter(buddy=buddy).order_by('date'),
        'principals': SecurityPrincipal.objects.filter(buddy=buddy).order_by('since'),
        }

@view_GET( r'^account/detail/(?P<id>[0-9]*)$', template = 'account_detail.html')
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
def transaction_detail(request, id, **kw):
    transaction = LogicTransaction.objects.get(id=id)
    return {
        'transaction': transaction,
        'splits': LogicTransactionSplit.objects.filter(transaction=transaction)
        }