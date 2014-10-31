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
    from roster.models import Buddy,BuddyEvent,SecurityPrincipal

    return {
        'users':
            ((buddy,BuddyEvent.objects.filter(buddy=buddy),SecurityPrincipal.objects.filter(buddy=buddy))
                for buddy in Buddy.objects.all().order_by('nickname')),
    }

@view_GET( r'^roster/user/(?P<uid>[0-9]*)$', template = 'roster_user.html')
def roster_user(request, uid, **kw):
    from roster.models import Buddy,BuddyEvent,SecurityPrincipal
    buddy = Buddy.objects.get(uid=int(uid))
    return {
        'user': buddy,
        'events': BuddyEvent.objects.filter(buddy=buddy).order_by('date'),
        'principals': SecurityPrincipal.objects.filter(buddy=buddy).order_by('since'),
    }