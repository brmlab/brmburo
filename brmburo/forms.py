from django import forms
from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapPasswordInput
from django.contrib.admin import ModelAdmin

from buddies import get_default_prime
from brmburo.models import Buddy
import widgets


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

    def __init__(self, *args, **kwargs):
        super(BuddyAdminForm, self).__init__(*args, **kwargs)
        self.fields['uid'].initial = get_default_prime()


class BuddyAdmin(ModelAdmin):
    form = BuddyAdminForm


class BuddyForm(widgets.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BuddyForm, self).__init__(*args, **kwargs)
        self.fields['uid'].initial = get_default_prime()

    class Meta:
        model = Buddy
        fields = ('uid', 'type', 'first_name', 'middle_name', 'surname', 'nickname', 'email', 'phone', 'born', 'irl', 'comment', 'user')
        attrs = {
            'uid': {
                'label': 'Unique prime',
                'widget': widgets.Uneditable(),
                }
        }
