import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brmburo.settings')

from brmburo.transactions import account_sum
from brmburo.models import Buddy

import datetime
import logging

logger = logging.getLogger(__name__)


for buddy in Buddy.objects.all().order_by('nickname'):
    if buddy.logic_account is None:
        continue
    template = u'Balance for @%(nickname)s is %(balance)s %(curr)s.'
    #template = u'@%(nickname)s\t%(balance)s\t%(curr)s'
    logger.info(template % dict(
        curr = buddy.logic_account.currency.symbol,
        nickname = buddy.nickname,
        balance = account_sum(buddy),
    ))