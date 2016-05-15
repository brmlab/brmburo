
__author__ = 'pborky'

from bootstrap_toolkit.widgets import add_to_css_class
from django.forms import TextInput, ModelForm
from django.utils.safestring import mark_safe
from brmburo.models import Buddy
from django.contrib.admin import ModelAdmin
from django.db.models import Max
from helpers import rabin_miller

class FormfieldCallback(object):
    def __init__(self, meta=None, **kwargs):
        if meta is None:
            self.attrs = {}
        elif isinstance(meta, dict):
            self.attrs = meta
        elif hasattr(meta, 'attrs'):
            self.attrs = meta.attrs
        else:
            raise TypeError('Argument "meta" must be dict or must contain attibute "attrs".')
        self.attrs.update(kwargs)

    def __call__(self, field, **kwargs):
        if field.name in self.attrs:
            kwargs.update(self.attrs[field.name])
        queryset_transform = kwargs.pop('queryset_transform', None)
        if callable(queryset_transform):
            pass #field.choices = queryset_transform(field.choices)
        return field.formfield(**kwargs)

class BuddyAdminForm(ModelForm):
    class Meta:
        model = Buddy

    @staticmethod
    def get_default_prime():
        #select max UID we have or start with 3 as largest previous prime
        prime_candidate = Buddy.objects.all().aggregate(Max('uid'))['uid__max'] or 3
        prime_candidate |= 1 #just make sure we start with odd number if something was broken in DB
        while True:
            prime_candidate += 2
            if rabin_miller(prime_candidate):
                return prime_candidate

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("initial"): #apply only for "add buddy" functionality
            kwargs['initial'].update({'uid': BuddyAdminForm.get_default_prime()})
        super(BuddyAdminForm, self).__init__(*args, **kwargs)

class Uneditable(TextInput):
    def __init__(self, value_calback=None, choices=(), *args,  **kwargs):
        super(Uneditable, self).__init__(*args, **kwargs)
        self.value_calback = value_calback
        self.choices = list(choices)
        self.attrs['disabled'] = True

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['type'] = 'hidden'
        klass = add_to_css_class(self.attrs.pop('class', ''), 'uneditable-input')
        klass = add_to_css_class(klass, attrs.pop('class', ''))

        base = super(Uneditable, self).render(name, value, attrs)
        if not isinstance(value, list):
            value = [value]
        if self.value_calback:
            if not hasattr(self, 'choices') or isinstance(self.choices, list):
                value = self.value_calback(None, value)
            else:
                value = self.value_calback(self.choices.queryset, value)
        if isinstance(value,list):
            if not value:
                value =  u'<span class="%s" style="color: #555555; background-color: #eeeeee;" disabled="true"></span>' % klass
            else:
                value =  u''.join(u'<span class="%s" style="color: #555555; background-color: #eeeeee;" disabled="true">%s</span>' % (klass, val) for val in value)
        else:
            value = u'<span class="%s" style="color: #555555; background-color: #eeeeee;" disabled="true">%s</span>' % (klass, value)
        return mark_safe(base + value)

class BuddyAdmin(ModelAdmin):
    ordering = ('nickname',)
    form = BuddyAdminForm

