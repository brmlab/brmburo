import logging

from django.utils.timezone import now

from datetime import timedelta
from project.roster.models import LogicAccount, LogicTransaction, LogicTransactionSplit, Buddy, BuddyEvent


logger = logging.getLogger(__name__)

PREPAID = LogicAccount.objects.get(symbol='prepaid')
INCOME = LogicAccount.objects.get(symbol='income')
CONVERSE = dict(
    CZK = LogicAccount.objects.get(symbol='czk', type__symbol='converse'),
    EUR = LogicAccount.objects.get(symbol='eur', type__symbol='converse'),
    USD = LogicAccount.objects.get(symbol='usd', type__symbol='converse'),
)

PAYMENT = dict(
    CZK=500,
    EUR=20,
    USD=30,
)
DISCOUNT_FACTORS = dict(
    discount25=0.75,
    discount50=0.50,
    discount75=0.25,
    discount=0.,
)

def payment_due(buddy):
    time = now()

    buddy_logic_account = buddy.logic_account

    if buddy_logic_account is None:
        return None, None

    # if already issued in past 28 days return that transaction
    lts = LogicTransactionSplit.objects.filter(
        account = buddy_logic_account,
        transaction__time__gt=time-timedelta(28.),
        side=1,  # credit
    )
    if lts.exists():
        return lts[0].transaction, buddy

    ammount = PAYMENT.get('CZK')

    # get valid discount events and calculate discount
    be = BuddyEvent.objects.filter(
        buddy=buddy,
        date__gte=time,        # valid now
        until__lte=time,
        until__isnull=False,
        type__symbol__startswith='discount',
    )
    if be.exists():
        if be.count() > 1:
            raise Exception('Only one concurent discount is allowed.')
        ammount *= DISCOUNT_FACTORS.get(be[0].type.symbol, 1.)

    # transaction
    lt = LogicTransaction(
        time=time,
        comment='Credit @%s\'s monthly membership fee.' % buddy.nickname
    )
    lt.save()

    # splits
    LogicTransactionSplit(
        transaction = lt,
        side = 1,
        account = buddy_logic_account,
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

    return lt, buddy

def payment_income(bank_transaction, buddy=None):
    time = now()

    if buddy is None:
        buddies = Buddy.objects.filter(uid=bank_transaction.variable_symbol)
        # no buddy - no transaction
        if not buddies.exists():
            return None, None
        buddy, = buddies

    # if already linked with logic transaction return that one
    if bank_transaction.logic_transaction is not None:
        return bank_transaction.logic_transaction, buddy

    # no account - no transaction
    buddy_logic_account = buddy.logic_account
    if buddy_logic_account is None:
        return None, None

    # no account - no transaction
    bank_logic_account = bank_transaction.my_account.logic_account
    if bank_logic_account is None:
        return None, None

    amount = bank_transaction.amount

    if bank_transaction.currency.symbol == 'EUR':
        amount_czk = amount * PAYMENT.get('CZK') / PAYMENT.get('EUR')
    elif bank_transaction.currency.symbol == 'USD':
        amount_czk = amount * PAYMENT.get('CZK') / PAYMENT.get('USD')
    else:
        amount_czk = amount

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
        amount = amount_czk,
        comment = '',
    ).save() #debit
    LogicTransactionSplit(
        transaction = lt,
        side = 1,
        account = PREPAID,
        amount = amount_czk,
        comment = '',
    ).save() #credit
    LogicTransactionSplit(
        transaction = lt,
        side = -1,
        account = INCOME,
        amount = amount_czk,
        comment = '',
    ).save() #debit

    # additional splits for foreign currencies
    if bank_transaction.currency.symbol in ( 'EUR', 'USD', ): # convert to CZK
        LogicTransactionSplit(
            transaction = lt,
            side = 1,
            account = CONVERSE.get('CZK'),
            amount = amount_czk,
            comment = '',
        ).save() #credit

    if bank_transaction.currency.symbol == 'EUR': # convert from EUR
        LogicTransactionSplit(
            transaction = lt,
            side = -1,
            account = CONVERSE.get('EUR'),
            amount = amount,
            comment = '',
        ).save() #debit

    if bank_transaction.currency.symbol == 'USD': # convert from USD
        LogicTransactionSplit(
            transaction = lt,
            side = -1,
            account = CONVERSE.get('USD'),
            amount = amount,
            comment = '',
        ).save() #debit

    bank_transaction.logic_transaction = lt
    bank_transaction.save()

    logger.info('Payment from user @%s.'%buddy.nickname)

    return lt, buddy

def account_sum(logic_account):
    if isinstance(logic_account, Buddy):
        logic_account = logic_account.logic_account
    lts = LogicTransactionSplit.objects.filter(
        account=logic_account
    )
    return reduce(lambda acc, la: acc+la.side*la.amount, lts, 0)


