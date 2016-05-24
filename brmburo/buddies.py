from decimal import Decimal
import logging

from django.utils.timezone import now
from django.db.models import Q

from datetime import timedelta
from models import LogicAccount, LogicAccountType, LogicTransaction, LogicTransactionSplit, Buddy, BuddyEvent, Currency


logger = logging.getLogger(__name__)


def buddy_after_create(buddy):
    if buddy.type.symbol == 'member':
        buddy.logic_account = LogicAccount.objects.create(
            name = "Payments from %s %s" % (buddy.first_name, buddy.surname),
            symbol = "@%s" % buddy.nickname,
            currency = Currency.objects.get(symbol="CZK"),
            type = LogicAccountType.objects.get(symbol = "credit")
        )
    buddy.save()
    if buddy.type.symbol == 'member':
        event = BuddyEvent.objects.create(
            buddy=buddy,
            type=BuddyEventType.objects.create(symbol = 'start'),
            date=now(),
            reason="Buddy %s created" % buddy.nickname,
        )
    event.save()

