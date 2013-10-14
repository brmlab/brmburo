__author__ = 'pborky'

from django.db.models import Model, CharField, EmailField, IntegerField, BooleanField, DateField, TextField, ForeignKey, ManyToManyField, FileField, DateTimeField
from django.utils.datetime_safe import date

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
    def __unicode__(self):
        template = u'@%s (%s %s %s)' if self.type.is_member else u' %s (%s %s %s)'
        return template % tuple(map(lambda x: '' if x is None else x, (self.nickname, self.first_name, self.middle_name, self.surname)))
    class Meta:
        ordering = ["type", "nickname"]
        verbose_name = "_Buddy"
        verbose_name_plural = "_Buddies"


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
    duration = IntegerField(verbose_name='Duration of Event', blank=True, null=True) # e.g. for discount otherwise null
    value = IntegerField(verbose_name='Integer Value', blank=True, null=True) # e.g. for discount otherwise null
    reason = TextField(max_length=1000, verbose_name='Reason', blank=True, null=True )
    attachments = ManyToManyField(Attachment, blank=True, null=True)
    def __unicode__(self):
        template = u'%s -> %s'
        return template % (self.buddy, self.type)
    class Meta:
        ordering = ["-date", "buddy"]
        verbose_name = "_Buddy Event"

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
        verbose_name = "_Security Principal"


