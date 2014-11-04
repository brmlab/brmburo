# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'roster_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'roster', ['Currency'])

        # Adding model 'Transaction'
        db.create_table(u'roster_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('my_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='my', to=orm['roster.Account'])),
            ('their_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='their', to=orm['roster.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Currency'])),
            ('constant_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('specific_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('variable_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('recipient_message', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('buddy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Buddy'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'roster', ['Transaction'])

        # Adding model 'Account'
        db.create_table(u'roster_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('bank_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('account_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'roster', ['Account'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'roster_currency')

        # Deleting model 'Transaction'
        db.delete_table(u'roster_transaction')

        # Deleting model 'Account'
        db.delete_table(u'roster_account')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'roster.account': {
            'Meta': {'ordering': "['bank_code', 'account_number']", 'object_name': 'Account'},
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'bank_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'roster.attachment': {
            'Meta': {'ordering': "['-date', 'name']", 'object_name': 'Attachment'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'roster.buddy': {
            'Meta': {'ordering': "['type', 'nickname']", 'object_name': 'Buddy'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['roster.Attachment']", 'null': 'True', 'blank': 'True'}),
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.BuddyType']"}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'roster.buddyevent': {
            'Meta': {'ordering': "['-date', 'buddy']", 'object_name': 'BuddyEvent'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['roster.Attachment']", 'null': 'True', 'blank': 'True'}),
            'buddy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Buddy']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.BuddyEventType']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'roster.buddyeventtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'BuddyEventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'roster.buddytype': {
            'Meta': {'ordering': "['-is_member', 'name']", 'object_name': 'BuddyType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'roster.currency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Currency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'roster.principaltype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PrincipalType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'roster.securityprincipal': {
            'Meta': {'ordering': "['-since', 'buddy']", 'object_name': 'SecurityPrincipal'},
            'buddy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Buddy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'since': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.PrincipalType']"}),
            'until': ('django.db.models.fields.DateField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'max_length': '1000'})
        },
        u'roster.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'buddy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Buddy']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'constant_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roster.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my'", 'to': u"orm['roster.Account']"}),
            'recipient_message': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'specific_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'their_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'their'", 'to': u"orm['roster.Account']"}),
            'tid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'variable_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['roster']