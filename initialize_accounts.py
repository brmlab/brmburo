import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brmburo.settings')

from brmburo.transactions import payment_income, account_sum, payment_due
from brmburo.models import *

import datetime
import logging

import csv

fh = logging.FileHandler('initialize_accounts.log')
fh.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fh)


with open('bukake.csv') as f:
    bukake = dict( (int(k),int(v)) for k, v in csv.reader(f))


DUES = LogicAccount.objects.get(symbol='dues')
START_DATE = datetime.date(year=2014, month=12, day=31)

for uid, amount_czk in bukake.items():
    buddy = Buddy.objects.get(uid=uid)
    buddy_logic_account = buddy.logic_account


    # transaction
    lt = LogicTransaction(
        time=START_DATE,
        comment=u'Initial balance for @%s.' % buddy.nickname,
        )
    lt.save()

    side = 1 if amount_czk >= 0 else -1
    amount_czk = abs(amount_czk)

    # splits
    lts = LogicTransactionSplit(
        transaction = lt,
        side = -side,
        account = DUES,
        amount = amount_czk,
        comment = '',
        )
    lts.save() #credit
    lts = LogicTransactionSplit(
        transaction = lt,
        side = side,
        account = buddy_logic_account,
        amount = amount_czk,
        comment = '',
        )
    lts.save() #debit

    template = u'Initial balance %(amount)0.2f[%(curr)s] for @%(nickname)s accounted as transaction #%(tid)d. New balance for @%(nickname)s is %(balance)s %(curr)s.'
    logger.info(template % dict(
        amount=lts.amount_(),
        curr=lts.account.currency.symbol,
        nickname=buddy.nickname,
        tid=lts.transaction.id,
        balance=account_sum(buddy),
    ))

for year, month in [(2015, 1), (2015, 2), (2015, 3), (2015, 4), (2015, 5), (2015, 6), (2015, 7), (2015, 8), (2015, 9),
                    (2015, 10), (2015, 11), (2015, 12)]:

    logger.info(u'Processing month %d/%d' % (month, year))

    for t in BankTransaction.objects.filter(logic_transaction__isnull=True, date__year=year, date__month=month):

        lt, b = payment_income(t)
        if lt is not None and b is not None:
            template = u'Paired incomming payment %(amount)0.2f[%(curr1)s] from @%(nickname)s accounted as transaction #%(tid)d. New balance for @%(nickname)s is %(balance)s %(curr2)s.'
            logger.info(template % dict(
                amount=t.amount,
                curr1=t.currency.symbol,
                curr2=b.logic_account.currency.symbol,
                nickname=b.nickname,
                tid=lt.id,
                balance=account_sum(b),
            ))
        else:
            logger.info(u'Not paired bank transaction #%s, ammount %0.2f.' % (t.tid, t.amount))

    for buddy in Buddy.objects.all():
        lt, b = payment_due(buddy, datetime.date(year=year, month=month, day=28))
        if lt is not None and b is not None:
            lts = LogicTransactionSplit.objects.get(transaction=lt, account=b.logic_account)
            template = u'Membership fee %(amount)0.2f %(curr)s for @%(nickname)s accounted as transaction #%(tid)d. New balance for @%(nickname)s is %(balance)s %(curr)s.'
            logger.info(template % dict(
                amount=lts.amount,
                curr=b.logic_account.currency.symbol,
                nickname=b.nickname,
                tid=lt.id,
                balance=account_sum(b),
            ))