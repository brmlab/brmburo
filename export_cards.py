#!/usr/bin/env python

import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brmburo.settings')
import logging
logger = logging.getLogger(__name__)
from django.utils.timezone import now
from brmburo.models import SecurityPrincipal


n = now()
for sp in SecurityPrincipal.objects.filter(since__lte=n,until__gt=n,buddy__type__symbol='member').order_by('buddy__nickname'):
        print sp.buddy.nickname, sp.value

