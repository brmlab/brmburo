__author__ = 'pborky'

from django.db.models import Model, CharField, EmailField, IntegerField, BooleanField, DateField, TextField, ForeignKey, ManyToManyField, FileField, DateTimeField
from tinymce.models import HTMLField

class SiteResource(Model): # some resource strings
    name = CharField(max_length=100, verbose_name='Name')
    value = HTMLField(verbose_name='Value')
    def __unicode__(self):
        return u'%s' %(self.name,)
    class Meta:
        ordering = ["name"]
        verbose_name = "Site Resource"

class BuddyType(Model): # friend, member, terminated, suspended ...
    name = CharField(max_length=100, verbose_name='Buddy Type Name')
    symbol = CharField(max_length=10)
    is_member = BooleanField(verbose_name='Is Member?')
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = [ "-is_member", "name" ]
        verbose_name = "Buddy Type"

class Attachment(Model):
    name = CharField(max_length=100, verbose_name='Attachment Name')
    date = DateTimeField(verbose_name='Created',auto_now=True)
    file = FileField(verbose_name='File', upload_to='/dev/null')  # TODO:
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = ["-date", "name"]
        verbose_name = "Attachment"

class Buddy(Model):
    uid = IntegerField(verbose_name='Unique Prime')
    type = ForeignKey(BuddyType) # friend, member, terminated, suspended
    first_name = CharField(max_length=100, verbose_name='First Name' )
    middle_name = CharField(max_length=100, verbose_name='Middle Name' )
    surname = CharField(max_length=100, verbose_name='Surname' )
    nickname = CharField(max_length=100, verbose_name='Nickname',unique=True )
    email = EmailField(max_length=100, verbose_name='Email' )
    phone =  CharField(max_length=30, verbose_name='Phone' )
    born = DateField(verbose_name='Year of Birth')
    irl = BooleanField(verbose_name='Present in Real Life?')
    #since = DateField(verbose_name='Member Since') # obsolete? - query BuddyEvents
    #until = DateField(verbose_name='Member Until') # obsolete? - query BuddyEvents
    comment = TextField(max_length=1000, verbose_name='Comment' )
    attachments = ManyToManyField(Attachment)
    # term_reason = TextField(max_length=1000, verbose_name='Termination Reason' ) # obsolete? - query BuddyEvents.reason
    def __unicode__(self):
        template = u'@%s (%s %s %s)' if self.type.is_member else u' %s'
        return template % (self.nickname,self.first_name, self.middle_name, self.surname)
    class Meta:
        ordering = ["type", "nickname"]
        verbose_name = "Buddy"
        verbose_name_plural = "Buddies"


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
    duration = IntegerField(verbose_name='Duration of Event') # e.g. for discount otherwise null
    value = IntegerField(verbose_name='Integer Value') # e.g. for discount otherwise null
    reason = TextField(max_length=1000, verbose_name='Reason' )
    attachments = ManyToManyField(Attachment)
    def __unicode__(self):
        template = u'%s -> %s'
        return template % (self.buddy, self.type)
    class Meta:
        ordering = ["-date", "buddy"]
        verbose_name = "Buddy Event"

class PrincipalType(Model): # gpg, ssh, physical key, card ..
    name = CharField(max_length=100, verbose_name='Key Type Name')
    symbol = CharField(max_length=10)
    def __unicode__(self):
        template = u'%s'
        return template % (self.name,)
    class Meta:
        ordering = [ "name" ]
        verbose_name = "Key Type"

class SecurityPrincipal(Model): # management of buddy's security principals - gpg keys, ssh keys, crads ..
    buddy = ForeignKey(Buddy)
    since = DateField(verbose_name='Start of Validity')
    until = DateField(verbose_name='End of Validity')
    type = ForeignKey(PrincipalType)
    value = TextField(max_length=1000, verbose_name='Key')
    def __unicode__(self):
        template = u'%s -> %s'
        return template % (self.buddy, self.type)
    class Meta:
        ordering = ["-start", "buddy"]
        verbose_name = "Security Principal"


