from functools import wraps
from django.core.paginator import Page, Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import available_attrs

import types
from django.contrib import messages
from django.views.decorators import http
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.conf.urls import url
from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from functional import partial

try:
    from .settings import ITEMS_PER_PAGE
except ImportError:
    ITEMS_PER_PAGE = 15

_HTTP_METHODS = ('get','post', 'option', 'put', 'delete', 'head')

def autoregister(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


class combine(dict):
    def __init__(self, *dicts):
        super(combine, self).__init__()
        self.dicts = dicts
    def get(self, item, default=None):
        for d in self.dicts:
            if item in d:
                return d[item]
        return default
    def __len__(self):
        return sum(len(d) for d in self.dicts)


class Decorator(object):
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
    def __call__(self, *args, **kwargs):
        return self.func.__call__(*args, **kwargs)


class NotAuthorizedException(Exception):
    pass

def view(pattern, template = None, template_401='401.html', form_cls = None, redirect_to = None, redirect_attr = None, invalid_form_msg = 'Form is not valid.', decorators = (), **kwargs):
    class Wrapper(Decorator):
        def __init__(self, obj):
            super(Wrapper, self).__init__(obj)

            if isinstance(obj, types.ClassType):
                obj = obj()

            def get_function(obj, name):
                if hasattr(obj, name):
                    fnc = getattr(obj, name)
                    if not isinstance(fnc, types.FunctionType): # we heave instance method
                        fnc = partial(fnc, obj)
                    return fnc

            if callable(obj):
                permitted_methods = dict((method.upper(), obj) for method in _HTTP_METHODS )
                require_http_methods_decorators = ()
            else:
                permitted_methods = dict(filter(None, ((method.upper(), get_function(obj,method)) for method in _HTTP_METHODS )))
                require_http_methods_decorators = http.require_http_methods(request_method_list=permitted_methods.keys()),


            for key, val in  permitted_methods.items():
                setattr(self, key.lower(), val)
            
            self.permitted_methods = permitted_methods.keys()

            # decorate inner function
            self.inner = reduce(lambda fnc, dec: dec(fnc), require_http_methods_decorators+decorators, self.inner )

        @staticmethod
        def _mk_forms(*args, **kwargs):
            if isinstance(form_cls,tuple) or isinstance(form_cls, list):
                return list(f(*args, **kwargs) for f in form_cls)
            elif isinstance(form_cls, dict):
                return dict((k,f(*args, **kwargs)) for k,f in form_cls.iteritems())
            else:
                if form_cls is not None:
                    return [form_cls(*args, **kwargs),]
                else:
                    return [None,]
        @staticmethod
        def _is_valid(forms):
            if isinstance(forms,dict):
                it = forms.itervalues()
            else:
                it = forms
            return all(f.is_valid() if f is not None else True for f in it)

        def url(self):
            return url(pattern, self, kwargs, self.__name__)

        def __call__(self, *args, **kwargs):
            return self.inner(*args, **kwargs)
            

        def inner(self, request, *args, **kwargs):
            from django.shortcuts import render, redirect
            try:

                if request.method not in self.permitted_methods:
                    return http.HttpResponseNotAllowed(permitted_methods=self.permitted_methods)

                if request.method in ('POST',):

                    forms = self._mk_forms(request.POST)
                    ret =  self.post(request, *args, forms=forms, **kwargs)

                    if isinstance(ret, HttpResponse):
                        return ret

                    if not self._is_valid(forms) and invalid_form_msg:
                        messages.error(request, invalid_form_msg)

                elif request.method in ('GET',) :

                    forms =  self._mk_forms()
                    # TODO setup forms from get paramters

                    ret =  self.get(request, *args, forms=forms, **kwargs)

                    if isinstance(ret, HttpResponse):
                        return ret

                    if not self._is_valid(forms):
                        #forms =  self._mk_forms()
                        #messages.error(request, invalid_form_msg)
                        pass

                elif request.method in ('HEAD', 'OPTION', 'PUT', 'DELETE') :
                    ret =  {}  # not implemented yet
                    forms =  self._mk_forms()

                else:
                    return

            except AttributeError as e:
                raise e
                #return HttpResponseServerError()
            except NotAuthorizedException:
                context_vars = { }
                context_vars.update(kwargs)
                return render(request, template_401, context_vars)

            redirect_addr = combine(request.GET, request.POST).get(redirect_attr, redirect_to)

            if redirect_addr:
                context_vars = { }

                context_vars.update(kwargs)

                if isinstance(ret,dict):
                    context_vars.update(ret)

                return redirect(redirect_addr, *args, **context_vars)
            else:
                context_vars = {
                            'forms': forms,
                        }
                context_vars.update(kwargs)

                if isinstance(ret,dict):
                    context_vars.update(ret)

                return render(request, template, context_vars)
    return Wrapper


def view_GET(*args, **kwargs):
    decorators = kwargs.pop('decorators', ())
    return view(*args, decorators=(require_GET,)+decorators , **kwargs)


def view_POST(*args, **kwargs):
    decorators = kwargs.pop('decorators', ())
    return view(*args, decorators=(require_POST,)+decorators , **kwargs)


def superuser_required(function):
    """
    Check if superuser is present, otherwise raise NotAuthorizedException.
    """
    @wraps(function, assigned=available_attrs(function))
    def inner(request, *a, **kw):
        if request.user.is_superuser:
            return function(request, *a, **kw)
        raise NotAuthorizedException('Superuser is required.')

    if callable(function):
        return inner

    raise ValueError('Not a function')


def staff_required(function):
    """
    Check if superuser is present, otherwise raise NotAuthorizedException.
    """
    @wraps(function, assigned=available_attrs(function))
    def inner(request, *a, **kw):
        if request.user.is_staff:
            return function(request, *a, **kw)
        raise NotAuthorizedException('Superuser is required.')

    if callable(function):
        return inner

    raise ValueError('Not a function')


class PageWrapper(object):
    """
    Wrap the page object of Page class and call callback for each item.
    Operates lazily unless __getitem__ is called.
    """
    def __init__(self, page, callback, lazy=True):
        if not callable(callback):
            raise ValueError('Not a function')
        if not isinstance(page, Page):
            raise ValueError('Not a Page')
        self._callback = callback
        self.page = page

    @property
    def number(self):
        return self.page.number

    @property
    def paginator(self):
        return self.page.paginator

    def __repr__(self):
        return repr(self.page)

    def __len__(self):
        return len(self.page)

    def __getitem__(self, index):
        return self._callback(self.page[index])

    def __iter__(self):
        return (self._callback(i) for i in self.page)

    def __contains__(self, value):
        return self.page.__contains__(value)

    def index(self, value):
        return self.page.index(value)

    def count(self, value):
        return self.page.count(value)

    def has_next(self):
        return self.page.has_next()

    def has_previous(self):
        return self.page.has_previous()

    def has_other_pages(self):
        return self.page.has_other_pages()

    def next_page_number(self):
        return self.page.next_page_number()

    def previous_page_number(self):
        return self.page.previous_page_number()

    def start_index(self):
        return self.page.start_index()

    def end_index(self):
        return self.page.end_index()


class LazyPageWrapper(PageWrapper):

    def __init__(self, page, callback):
        super(LazyPageWrapper, self).__init__(page, callback)

    def __getitem__(self, index):
        raise KeyError('Invalid for lazy operation')


def paginate(results, number=None, callback=None):
    paginator = Paginator(results, ITEMS_PER_PAGE)
    try:
        page = paginator.page(number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    if callable(callback):
        return LazyPageWrapper(page, callback)

    return page