import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.transactions import payment_due
from project.roster.models import Buddy

import datetime
import logging

logger = logging.getLogger(__name__)


for buddy in Buddy.objects.filter(type__symbol='member'):
    lt, b = payment_due(buddy)
    if lt is not None and b is not None:
        logger.info('Membership fee for user @%s accounted as transaction %d.' %( b.nickname, lt.id ))
