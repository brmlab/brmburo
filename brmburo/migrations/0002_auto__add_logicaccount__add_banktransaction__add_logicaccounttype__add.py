# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogicAccount'
        db.create_table(u'brmburo_logicaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.Currency'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicAccountType'])),
        ))
        db.send_create_signal(u'brmburo', ['LogicAccount'])

        # Adding model 'BankTransaction'
        db.create_table(u'brmburo_banktransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('my_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='my', to=orm['brmburo.BankAccount'])),
            ('their_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='their', to=orm['brmburo.BankAccount'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.Currency'])),
            ('constant_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('specific_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('variable_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('recipient_message', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('logic_transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicTransaction'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'brmburo', ['BankTransaction'])

        # Adding model 'LogicAccountType'
        db.create_table(u'brmburo_logicaccounttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicAccountType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['LogicAccountType'])

        # Adding model 'BuddyEvent'
        db.create_table(u'brmburo_buddyevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.Buddy'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.BuddyEventType'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['BuddyEvent'])

        # Adding M2M table for field attachments on 'BuddyEvent'
        db.create_table(u'brmburo_buddyevent_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('buddyevent', models.ForeignKey(orm[u'brmburo.buddyevent'], null=False)),
            ('attachment', models.ForeignKey(orm[u'brmburo.attachment'], null=False))
        ))
        db.create_unique(u'brmburo_buddyevent_attachments', ['buddyevent_id', 'attachment_id'])

        # Adding model 'Currency'
        db.create_table(u'brmburo_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal(u'brmburo', ['Currency'])

        # Adding model 'LogicTransaction'
        db.create_table(u'brmburo_logictransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['LogicTransaction'])

        # Adding model 'Buddy'
        db.create_table(u'brmburo_buddy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.BuddyType'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('born', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('irl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('logic_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicAccount'], null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['Buddy'])

        # Adding M2M table for field attachments on 'Buddy'
        db.create_table(u'brmburo_buddy_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('buddy', models.ForeignKey(orm[u'brmburo.buddy'], null=False)),
            ('attachment', models.ForeignKey(orm[u'brmburo.attachment'], null=False))
        ))
        db.create_unique(u'brmburo_buddy_attachments', ['buddy_id', 'attachment_id'])

        # Adding model 'BankAccount'
        db.create_table(u'brmburo_bankaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('bank_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('account_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.Currency'], null=True, blank=True)),
            ('logic_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicAccount'], null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['BankAccount'])

        # Adding model 'BuddyType'
        db.create_table(u'brmburo_buddytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'brmburo', ['BuddyType'])

        # Adding model 'Attachment'
        db.create_table(u'brmburo_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'brmburo', ['Attachment'])

        # Adding model 'SecurityPrincipal'
        db.create_table(u'brmburo_securityprincipal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.Buddy'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('since', self.gf('django.db.models.fields.DateField')()),
            ('until', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.PrincipalType'])),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal(u'brmburo', ['SecurityPrincipal'])

        # Adding model 'BuddyEventType'
        db.create_table(u'brmburo_buddyeventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'brmburo', ['BuddyEventType'])

        # Adding model 'PrincipalType'
        db.create_table(u'brmburo_principaltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'brmburo', ['PrincipalType'])

        # Adding model 'LogicTransactionSplit'
        db.create_table(u'brmburo_logictransactionsplit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicTransaction'])),
            ('side', self.gf('django.db.models.fields.IntegerField')()),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brmburo.LogicAccount'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'brmburo', ['LogicTransactionSplit'])


    def backwards(self, orm):
        # Deleting model 'LogicAccount'
        db.delete_table(u'brmburo_logicaccount')

        # Deleting model 'BankTransaction'
        db.delete_table(u'brmburo_banktransaction')

        # Deleting model 'LogicAccountType'
        db.delete_table(u'brmburo_logicaccounttype')

        # Deleting model 'BuddyEvent'
        db.delete_table(u'brmburo_buddyevent')

        # Removing M2M table for field attachments on 'BuddyEvent'
        db.delete_table('brmburo_buddyevent_attachments')

        # Deleting model 'Currency'
        db.delete_table(u'brmburo_currency')

        # Deleting model 'LogicTransaction'
        db.delete_table(u'brmburo_logictransaction')

        # Deleting model 'Buddy'
        db.delete_table(u'brmburo_buddy')

        # Removing M2M table for field attachments on 'Buddy'
        db.delete_table('brmburo_buddy_attachments')

        # Deleting model 'BankAccount'
        db.delete_table(u'brmburo_bankaccount')

        # Deleting model 'BuddyType'
        db.delete_table(u'brmburo_buddytype')

        # Deleting model 'Attachment'
        db.delete_table(u'brmburo_attachment')

        # Deleting model 'SecurityPrincipal'
        db.delete_table(u'brmburo_securityprincipal')

        # Deleting model 'BuddyEventType'
        db.delete_table(u'brmburo_buddyeventtype')

        # Deleting model 'PrincipalType'
        db.delete_table(u'brmburo_principaltype')

        # Deleting model 'LogicTransactionSplit'
        db.delete_table(u'brmburo_logictransactionsplit')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'brmburo.attachment': {
            'Meta': {'ordering': "['-date', 'name']", 'object_name': 'Attachment'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'brmburo.bankaccount': {
            'Meta': {'ordering': "['bank_code', 'account_number']", 'object_name': 'BankAccount'},
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'bank_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.Currency']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logic_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicAccount']", 'null': 'True', 'blank': 'True'})
        },
        u'brmburo.banktransaction': {
            'Meta': {'object_name': 'BankTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'constant_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logic_transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicTransaction']", 'null': 'True', 'blank': 'True'}),
            'my_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my'", 'to': u"orm['brmburo.BankAccount']"}),
            'recipient_message': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'specific_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'their_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'their'", 'to': u"orm['brmburo.BankAccount']"}),
            'tid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'variable_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'brmburo.buddy': {
            'Meta': {'ordering': "['type', 'nickname']", 'object_name': 'Buddy'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['brmburo.Attachment']", 'null': 'True', 'blank': 'True'}),
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logic_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicAccount']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.BuddyType']"}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'brmburo.buddyevent': {
            'Meta': {'ordering': "['-date', 'buddy']", 'object_name': 'BuddyEvent'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['brmburo.Attachment']", 'null': 'True', 'blank': 'True'}),
            'buddy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.Buddy']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.BuddyEventType']"}),
            'until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'brmburo.buddyeventtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'BuddyEventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'brmburo.buddytype': {
            'Meta': {'ordering': "['-is_member', 'name']", 'object_name': 'BuddyType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'brmburo.currency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Currency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'brmburo.logicaccount': {
            'Meta': {'ordering': "['type', 'name']", 'object_name': 'LogicAccount'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicAccountType']"})
        },
        u'brmburo.logicaccounttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LogicAccountType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicAccountType']", 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'brmburo.logictransaction': {
            'Meta': {'object_name': 'LogicTransaction'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'brmburo.logictransactionsplit': {
            'Meta': {'object_name': 'LogicTransactionSplit'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicAccount']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side': ('django.db.models.fields.IntegerField', [], {}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.LogicTransaction']"})
        },
        u'brmburo.principaltype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PrincipalType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'brmburo.securityprincipal': {
            'Meta': {'ordering': "['-since', 'buddy']", 'object_name': 'SecurityPrincipal'},
            'buddy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.Buddy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'since': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['brmburo.PrincipalType']"}),
            'until': ('django.db.models.fields.DateField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '1000'})
        },
        u'brmburo.siteresource': {
            'Meta': {'ordering': "['name']", 'object_name': 'SiteResource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('tinymce.models.HTMLField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['brmburo']