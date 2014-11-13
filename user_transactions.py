#!/usr/bin/env python

import os;os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.models import Buddy
from project.roster.transactions import account_sum
import sys
import argparse

import datetime
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='User balance and transactions.')
parser.add_argument('-u', '--user', action='append', help='user')
args = parser.parse_args()

users = args.user if isinstance(args.user,list) else [args.user]
buddies = Buddy.objects.filter(nickname__in=users)
for buddy in buddies:
    template = u'Balance for @%(nick)s is %(amount)0.2f %(currency)s.'
    print template % dict(
        nick = buddy.nickname,
        amount = account_sum(buddy),
        currency = 'CZK',
    )


