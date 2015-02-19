__author__ = 'pborky'

from django.db.models import Model, CharField, EmailField, IntegerField, BooleanField, DateField, TextField, ForeignKey, ManyToManyField, FileField, DateTimeField, FloatField, DecimalField
from tinymce.models import HTMLField
from django.utils.datetime_safe import date
from django.contrib.auth.models import User

class BuddyType(Model): # friend, member, terminated, suspended ...
    name = CharField(max_length=100, verbose_name='Buddy Type Name')
    symbol = CharField(max_length=10)
    is_member = BooleanField(verbose_name='Is Full Member?')
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = [ "-is_member", "name" ]
        verbose_name = "Buddy Type"

class Attachment(Model):
    name = CharField(max_length=100, verbose_name='Attachment Name')
    date = DateTimeField(verbose_name='Created',auto_now=True)
    file = FileField(verbose_name='File', upload_to='./attachments/')  # TODO:
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = ["-date", "name"]
        verbose_name = "Attachment"

class Buddy(Model):
    uid = IntegerField(verbose_name='Unique Prime')
    type = ForeignKey(BuddyType) # friend, member, terminated, suspended
    first_name = CharField(max_length=100, verbose_name='First Name', blank=True, null=True )
    middle_name = CharField(max_length=100, verbose_name='Middle Name', blank=True, null=True )
    surname = CharField(max_length=100, verbose_name='Surname', blank=True, null=True )
    nickname = CharField(max_length=100, verbose_name='Nickname',unique=True )
    email = EmailField(max_length=100, verbose_name='Email', blank=True, null=True )
    phone =  CharField(max_length=30, verbose_name='Phone', blank=True, null=True )
    born = DateField(verbose_name='Year of Birth', blank=True, null=True)
    irl = BooleanField(verbose_name='Present in Real Life?')
    #since = DateField(verbose_name='Member Since') # obsolete? - query BuddyEvents
    #until = DateField(verbose_name='Member Until') # obsolete? - query BuddyEvents
    comment = TextField(max_length=1000, verbose_name='Comment', blank=True, null=True )
    attachments = ManyToManyField(Attachment, blank=True, null=True)
    # term_reason = TextField(max_length=1000, verbose_name='Termination Reason' ) # obsolete? - query BuddyEvents.reason
    user = ForeignKey(User, blank=True, null=True)
    logic_account = ForeignKey('LogicAccount', blank=True, null=True)
    def __unicode__(self):
        template = u'@%s (%s %s %s)' if self.type.is_member else u' %s (%s %s %s)'
        return template % tuple(map(lambda x: '' if x is None else x, (self.nickname, self.first_name, self.middle_name, self.surname)))
    class Meta:
        ordering = ["type", "nickname"]
        verbose_name = "_Buddy"
        verbose_name_plural = "+Buddies"


class BuddyEventType(Model): # start, end, discount, termination, suspend
    name = CharField(max_length=100, verbose_name='Event Type Name')
    symbol = CharField(max_length=10)
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = ["name"]
        verbose_name = "Buddy Event Type"

class BuddyEvent(Model):
    buddy = ForeignKey(Buddy)
    type = ForeignKey(BuddyEventType)
    date = DateField(verbose_name='Event Start')
    until = DateField(verbose_name='Event End', blank=True, null=True) # e.g. for discount otherwise null
    reason = TextField(max_length=1000, verbose_name='Reason', blank=True, null=True )
    attachments = ManyToManyField(Attachment, blank=True, null=True)
    def __unicode__(self):
        template = u'%s -> %s'
        return template % (self.buddy, self.type)
    class Meta:
        ordering = ["-date", "buddy"]
        verbose_name = "+Buddy Event"

class PrincipalType(Model): # gpg, ssh, physical key, card ..
    name = CharField(max_length=100, verbose_name='Principal Type Name')
    symbol = CharField(max_length=10)
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = [ "name" ]
        verbose_name = "Key Type"

class SecurityPrincipal(Model): # management of buddy's security principals - gpg keys, ssh keys, crads ..
    buddy = ForeignKey(Buddy)
    name = CharField(max_length=100, verbose_name='Principal Name')
    since = DateField(verbose_name='Start of Validity')
    until = DateField(verbose_name='End of Validity')
    type = ForeignKey(PrincipalType)
    value = TextField(max_length=1000, verbose_name='Key')
    def is_valid(self):
        return self.since <= date.today() < self.until
    def __unicode__(self):
        template = u'%s -> %s' if self.is_valid() else u'%s -> %s [invalid]'
        return template % (self.buddy, self.type)
    class Meta:
        ordering = ["-since", "buddy"]
        verbose_name = "+Security Principal"

class Currency(Model):
    name = CharField(max_length=100, verbose_name='Currency Name')
    symbol = CharField(max_length=10, unique=True)
    def __unicode__(self):
        template = u'%s'
        return template % (self.symbol,)
    class Meta:
        ordering = [ "name" ]
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

class LogicAccountType(Model): # bank, income, expense, credit
    name = CharField(max_length=100, verbose_name='Logic Account Type Name')
    symbol = CharField(max_length=10, unique=True)
    parent = ForeignKey('LogicAccountType', blank=True, null=True)
    def __unicode__(self):
        template = u'%s'
        return template % (self.symbol,)
    class Meta:
        ordering = ["name"]
        verbose_name = "Logic Account Type"

class LogicAccount(Model):
    name = CharField(max_length=100, verbose_name='Logic Account Name',null=True,blank=True)
    symbol = CharField(max_length=20, unique=True)
    currency = ForeignKey(Currency)
    type = ForeignKey(LogicAccountType)
    def __unicode__(self):
        template = u'%s:%s[%s]'
        return template % (self.type, self.name, self.currency,)
    class Meta:
        ordering = [ "type", "name" ]

class LogicTransaction(Model):
    time = DateTimeField(verbose_name='Time')
    comment = CharField(max_length=255, verbose_name='Transaction Description',null=True,blank=True)
    def __unicode__(self):
        template = u'%s:%s'
        return template % (self.time.strftime('%Y-%m-%d %H:%M'), self.comment)
    class Model:
        ordering = [ "time" ]
        get_latest_by = 'time'


class LogicTransactionSplit(Model):
    transaction = ForeignKey(LogicTransaction)
    side = IntegerField(choices=((1, 'credit'), (-1, 'debit')), verbose_name='Debit/Credit Flag')
    account = ForeignKey(LogicAccount)
    amount = DecimalField(max_digits=8, decimal_places=2)
    comment = CharField(max_length=255, verbose_name='Transaction Split Description',null=True,blank=True)
    def amount_(self):
        return self.side * self.amount
    def __unicode__(self):
        template = u'%s %s %.2f (%s)'
        return template % (self.account, self.side, self.amount, self.comment)
    class Model:
        ordering = [ "tid", "side", "time" ]
        get_latest_by = 'tid'


class BankAccount(Model):
    account_number = CharField(max_length=20, verbose_name='Bank Account Number')
    bank_code = CharField(max_length=20, verbose_name='Bank Code')
    account_name  = CharField(max_length=100, verbose_name='Bank Account Name',null=True,blank=True)
    currency = ForeignKey(Currency, null=True, blank=True)
    logic_account = ForeignKey(LogicAccount, null=True, blank=True)
    def __unicode__(self):
        template = u'%s/%s[%s]'
        return template % (self.account_number,self.bank_code,self.currency or '',)
    class Meta:
        ordering = [ "bank_code", "account_number" ]

class BankTransaction(Model):
    tid = CharField(max_length=100, verbose_name='Bank Transaction ID',unique=True)
    my_account = ForeignKey(BankAccount,related_name='my')
    their_account = ForeignKey(BankAccount,related_name='their')
    amount = DecimalField(max_digits=8, decimal_places=2)
    currency = ForeignKey(Currency)
    constant_symbol = CharField(max_length=20, verbose_name='Constant Symbol',null=True,blank=True)
    specific_symbol = CharField(max_length=20, verbose_name='Specific Symbol',null=True,blank=True)
    variable_symbol = CharField(max_length=20, verbose_name='Variable Symbol',null=True,blank=True)
    recipient_message  = CharField(max_length=100, verbose_name='Recipient Message',null=True,blank=True)
    comment = CharField(max_length=100, verbose_name='Comment',null=True,blank=True)
    logic_transaction = ForeignKey(LogicTransaction, null=True, blank=True)
    #buddy = ForeignKey(Buddy,null=True,blank=True)
    date = DateField(verbose_name='Bank Transaction Date')
    def __unicode__(self):
        if self.amount >= 0:
            template = u'%0.2f %s (%s -> %s)'
        else:
            template = u'%0.2f %s (%s <- %s)'
        return template % (self.amount, self.currency, self.their_account, self.my_account)
    class Model:
        ordering = [ "date", "my_account" ]
        get_latest_by = 'date'

# Example - paying dues is a four-split transaction:
# bank         CREDIT 500
# pasky        DEBIT  500   (pasky's balance is debite when he pays since brmlab owes him money)
# prepaid_dues CREDIT 500
# income       DEBIT  500   (income is a debit account because magic)
# (we throw it into income immediately so that we can do stuff with
# the prepaid money, like giving them away in grants; but if
# prepaid_dues >= income (modulo credit/debit sign), we are of course
# in trouble)
#
# Accounting dues (at the 10th day of the month) is a transaction:
# pasky        CREDIT 500   (if pasky's balance ends up positive, he owes us money)
# prepaid_dues DEBIT  500   (if members globally don't pay their dues, this account could get negative)



class SiteResource(Model): # some resource strings
    name = CharField(max_length=100, verbose_name='Name')
    value = HTMLField(verbose_name='Value')
    def __unicode__(self):
        return u'%s' %(self.name,)
    class Meta:
        ordering = ["name"]
        verbose_name = "Site Resource"
