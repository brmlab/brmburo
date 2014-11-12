from django.utils.timezone import now
from project.roster.models import LogicAccount, LogicTransaction, LogicTransactionSplit, Buddy, BuddyEvent

import logging

logger = logging.getLogger(__name__)

PREPAID = LogicAccount.objects.get(symbol='prepaid')
INCOME = LogicAccount.objects.get(symbol='income')
PAYMENT = dict(
    CZK=500.,
    EUR=20.,
    USD=30.,
)
DISCOUNT_FACTORS = dict(
    discount25=0.75,
    discount50=0.50,
    discount75=0.25,
    discount=0.,
)

def payment_due(buddy):
    time = now()

    la = buddy.logic_account

    if la is None:
        return None

    # if already issued in past 28 days return that transaction
    lts = LogicTransactionSplit.objects.filter(account = la, transaction__time=time-28, )
    if lts.exists():
        return lts[0].transaction

    # get valid discount events and calculate discount
    be = BuddyEvent.objects.filter(
        buddy=buddy,
        date__ge=time,        # valid now
        until__le=time,
        until__isnull=False,
        type__symbol__startswith='discount'
    )
    if be.exists():
        if be.count() > 1:
            raise Exception('Only one concurent discount is allowed.')
        ammount = PAYMENT.get('CZK')*DISCOUNT_FACTORS.get(be[0].type.symbol, 1.)
    else:
        ammount = PAYMENT

    # transaction
    lt = LogicTransaction(
        time=time,
        comment='Credit @%s\'s monthly membership fee.'
    )
    lt.save()

    # splits
    LogicTransactionSplit(
        transaction = lt,
        side = 1,
        account = la,
        amount = ammount,
        comment = '',
    ).save() #credit
    LogicTransactionSplit(
        transaction = lt,
        side = -1,
        account = PREPAID,
        amount = ammount,
        comment = '',
    ).save() #debit

    logger.info('Payment due for user @%s.'%buddy.nickname)

    return lt

def payment_income(bank_transaction, buddy=None):
    time = now()

    if buddy is None:
        buddies = Buddy.objects.filter(uid=bank_transaction.variable_symbol)
        # no buddy - no transaction
        if not buddies.exists():
            return None
        buddy, = buddies

    # if already linked with logic transaction return that one
    if bank_transaction.logic_transaction is not None:
        return bank_transaction.logic_transaction

    # no account - no transaction
    buddy_logic_account = buddy.logic_account
    if buddy_logic_account is None:
        return None

    # no account - no transaction
    bank_logic_account = bank_transaction.my_account.logic_account
    if bank_logic_account is None:
        return None

    amount = bank_transaction.amount

    # transaction
    lt = LogicTransaction(
        time=bank_transaction.date,
        comment='Payment from @%s via bank.' % buddy.nickname,
    )
    lt.save()

    # splits
    LogicTransactionSplit(
        transaction = lt,
        side = 1,
        account = bank_logic_account,
        amount = amount,
        comment = (' /// '.join(filter(None,(bank_transaction.comment, bank_transaction.recipient_message))))[:100],
    ).save() #credit
    LogicTransactionSplit(
        transaction = lt,
        side = -1,
        account = buddy_logic_account,
        amount = amount,
        comment = '',
    ).save() #debit
    LogicTransactionSplit(
        transaction = lt,
        side = 1,
        account = PREPAID,
        amount = amount,
        comment = '',
    ).save() #credit
    LogicTransactionSplit(
        transaction = lt,
        side = -1,
        account = INCOME,
        amount = amount,
        comment = '',
    ).save() #debit

    bank_transaction.logic_transaction = lt
    bank_transaction.save()

    logger.info('Payment from user @%s.'%buddy.nickname)

    return lt

