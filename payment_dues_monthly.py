import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.transactions import payment_due
from project.roster.models import Buddy
from project import settings
from fiobank import FioBank
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal

from time import sleep
import datetime
import logging

logger = logging.getLogger(__name__)


for buddy in Buddy.objects.filter(type__symbol='member'):
    payment_due(buddy)
