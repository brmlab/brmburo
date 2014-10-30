import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from project.roster.models import BankTransaction, Currency, BankAccount, Buddy
from project import settings
from fiobank import FioBank
from django.core.exceptions import ObjectDoesNotExist

from time import sleep
import datetime
import logging

FIRST_DATE = datetime.date(2010, 9, 1)
logger = logging.getLogger(__name__)



for token in settings.BANK_TOKENS:
    client = FioBank(token=token)
    info = client.info()
    my,created = BankAccount.objects.get_or_create(account_number=info['account_number'], bank_code=info['bank_code'])
    if created:
        my.save()
    logger.info('Processing account %s...' % my)
    try:
        from_id = BankTransaction.objects.filter(my_account=my).latest('date').tid
        sleep(30) # to avoid HTTP 409 - "Conflict" response
        trans = client.last(from_id=from_id)
    except ObjectDoesNotExist:
        sleep(30) # to avoid HTTP 409 - "Conflict" response
        trans = client.last(from_date=FIRST_DATE)

    for tran in trans:
        tid =  tran.get('transaction_id')
        if BankTransaction.objects.filter(tid=tid).exists():
            logger.warning('Transaction %s already here.'%tid)
            continue

        if 'account_number' not in tran or  'bank_code' not in  tran:
            continue

        acc,created = BankAccount.objects.get_or_create(account_number=tran['account_number'], bank_code=tran['bank_code'])
        if created:
            acc.account_name = tran.get('account_name')
            acc.save()

        curr,created = Currency.objects.get_or_create(symbol=tran.get('currency'))
        if created:
            curr.name = curr.symbol
            curr.save()

        t = BankTransaction.objects.create(
            tid = tran.get('transaction_id'),
            my_account = my,
            their_account = acc,
            amount = tran.get('amount'),
            currency = curr,
            constant_symbol = tran.get('constant_symbol'),
            specific_symbol = tran.get('specific_symbol'),
            variable_symbol = tran.get('variable_symbol'),
            recipient_message = tran.get('recipient_message'),
            comment = tran.get('comment'),
            date = tran.get('date'),
        )

        buddy=Buddy.objects.filter(uid=t.variable_symbol)
        if buddy.exists():
            t.buddy = buddy[0]

        t.save()
        logger.info('Imported transaction %s.' % t)


