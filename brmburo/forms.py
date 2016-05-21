__author__ = 'pborky'

from random import shuffle
from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapPasswordInput
from brmburo.models import Buddy
from django.contrib.admin import ModelAdmin
from django.db.models import Max
from helpers import rabin_miller

class LoginForm(forms.Form):

    username = forms.CharField (
        label='',
        max_length=100,
        required=True,
        widget=BootstrapTextInput(attrs={'placeholder': 'Username'}),
    )
    password = forms.CharField (
        label='',
        max_length=100,
        required=True,
        widget=BootstrapPasswordInput(attrs={'placeholder': 'Password'}),
    )

class BuddyAdminForm(forms.ModelForm):
    class Meta:
        model = Buddy

    @staticmethod
    def get_default_prime():
        #select uid in range [1111,9999] that is not already taken
        buddy_uids = set(Buddy.objects.values_list('uid', flat=True))
        candidates = range(1111, 9999, 2)
        shuffle(candidates)

        for prime_candidate in candidates:
            if prime_candidate in buddy_uids:
                continue
            if rabin_miller(prime_candidate):
                return prime_candidate

    def __init__(self, *args, **kwargs):
        if kwargs.has_key("initial"): #apply only for "add buddy" functionality
            kwargs['initial'].update({'uid': BuddyAdminForm.get_default_prime()})
        super(BuddyAdminForm, self).__init__(*args, **kwargs)

class BuddyAdmin(ModelAdmin):
    form = BuddyAdminForm

