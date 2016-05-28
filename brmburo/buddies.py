import logging
import random

from django.utils.timezone import now
from random import shuffle

from models import LogicAccount, LogicAccountType, Buddy, BuddyEvent, BuddyEventType, Currency


logger = logging.getLogger(__name__)


def buddy_for_logic_account(account):
    buddy = Buddy.objects.filter(logic_account=account)
    return buddy[0] if buddy.exists() else None


def after_create_buddy(buddy):
    if buddy.type.symbol == 'member':
        buddy.logic_account = LogicAccount.objects.create(
            name="Payments from %s %s" % (buddy.first_name, buddy.surname),
            symbol="@%s" % buddy.nickname,
            currency=Currency.objects.get(symbol="CZK"),
            type=LogicAccountType.objects.get(symbol="credit")
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


def rabin_miller(num):
    """
    :param num: number to test
    :return: Returns if number is a prime according to Rabin-Miller primality test
    """

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5): # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % num
    return True

def get_default_prime():
    #select uid in range [1111,9999] that is not already taken
    buddy_uids = set(Buddy.objects.values_list('uid', flat=True))
    candidates = range(1111, 9999, 2)
    shuffle(candidates)

    for prime_candidate in candidates:
        if prime_candidate in buddy_uids:
            continue
        if rabin_miller(prime_candidate):
            return prime_candidate