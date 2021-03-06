from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
import tinymce.urls

from .helpers import autoregister
from .views import login,logout,login,do_login, roster, roster_user, account_detail, account_list, transaction_list, \
    transaction_detail, bank_transaction_list, bank_transaction_detail, bank_transaction_ignore, buddy_add, \
    buddy_add_new, get_attachment
from .models import Buddy
from .forms import BuddyAdmin

admin.autodiscover()
admin.site.register(Buddy, BuddyAdmin)

autoregister('brmburo')

urlpatterns = patterns('',
    do_login.url(),
    login.url(),
    logout.url(),
    roster.url(),
    roster_user.url(),
    account_detail.url(),
    account_list.url(),
    transaction_detail.url(),
    transaction_list.url(),
    bank_transaction_list.url(),
    bank_transaction_detail.url(),
    bank_transaction_ignore.url(),
    buddy_add.url(),
    buddy_add_new.url(),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include(tinymce.urls), name='tinymce'),
    url(r'^media/attachments/', get_attachment)
)

