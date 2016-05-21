__author__ = 'pborky'

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

class BuddyAdmin(ModelAdmin):
    form = BuddyAdminForm

class AddBuddyForm(forms.ModelForm):

    class Meta:
        model = Buddy
        fields = ('uid', 'type', 'first_name', 'middle_name', 'surname', 'nickname', 'email', 'phone', 'born', 'irl', 'comment', 'user')