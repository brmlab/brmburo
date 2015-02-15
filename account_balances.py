import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.transactions import payment_due, account_sum
from project.roster.models import Buddy, LogicTransactionSplit

import datetime
import logging

logger = logging.getLogger(__name__)


for buddy in Buddy.objects.filter(type__symbol='member'):
    template = u'Balance for @%(nickname)s is %(balance)s %(curr)s.'
    logger.info(template % dict(
        curr = buddy.logic_account.currency.symbol,
        nickname = buddy.nickname,
        balance = account_sum(buddy),
    ))