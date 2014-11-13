import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.transactions import payment_due, account_sum
from project.roster.models import Buddy, LogicTransactionSplit

import datetime
import logging

logger = logging.getLogger(__name__)


for buddy in Buddy.objects.filter(type__symbol='member'):
    lt, b = payment_due(buddy)
    if lt is not None and b is not None:
        lts = LogicTransactionSplit.objects.get(transaction=lt, account=b.logic_account)
        template = u'Membership fee %(amount)0.2f %(curr)s for @%(nickname)s accounted as transaction #%(tid)d. New balance for @%(nickname)s is %(balance)s %(curr)s.'
        logger.info(template % dict(
            amount =   lts.amount,
            curr = b.logic_account.currency.symbol,
            nickname = b.nickname,
            tid = lt.id,
            balance = account_sum(b),
        ))