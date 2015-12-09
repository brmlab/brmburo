
#!/usr/bin/env python

import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brmburo.settings')

from brmburo.transactions import payment_due, account_sum
from brmburo.models import Buddy, LogicTransactionSplit

import datetime
import logging

logger = logging.getLogger(__name__)

from django.utils.timezone import now
from brmburo.models import *
n = now()
for sp in SecurityPrincipal.objects.filter(since__lt=n,until__gt=n,buddy__type__symbol='member'):
        print sp.buddy.nickname, sp.value

