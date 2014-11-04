# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BuddyType'
        db.create_table(u'roster_buddytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'roster', ['BuddyType'])

        # Adding model 'Attachment'
        db.create_table(u'roster_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'roster', ['Attachment'])

        # Adding model 'Buddy'
        db.create_table(u'roster_buddy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.BuddyType'])),
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
        ))
        db.send_create_signal(u'roster', ['Buddy'])

        # Adding M2M table for field attachments on 'Buddy'
        db.create_table(u'roster_buddy_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('buddy', models.ForeignKey(orm[u'roster.buddy'], null=False)),
            ('attachment', models.ForeignKey(orm[u'roster.attachment'], null=False))
        ))
        db.create_unique(u'roster_buddy_attachments', ['buddy_id', 'attachment_id'])

        # Adding model 'BuddyEventType'
        db.create_table(u'roster_buddyeventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'roster', ['BuddyEventType'])

        # Adding model 'BuddyEvent'
        db.create_table(u'roster_buddyevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Buddy'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.BuddyEventType'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'roster', ['BuddyEvent'])

        # Adding M2M table for field attachments on 'BuddyEvent'
        db.create_table(u'roster_buddyevent_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('buddyevent', models.ForeignKey(orm[u'roster.buddyevent'], null=False)),
            ('attachment', models.ForeignKey(orm[u'roster.attachment'], null=False))
        ))
        db.create_unique(u'roster_buddyevent_attachments', ['buddyevent_id', 'attachment_id'])

        # Adding model 'PrincipalType'
        db.create_table(u'roster_principaltype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'roster', ['PrincipalType'])

        # Adding model 'SecurityPrincipal'
        db.create_table(u'roster_securityprincipal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.Buddy'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('since', self.gf('django.db.models.fields.DateField')()),
            ('until', self.gf('django.db.models.fields.DateField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roster.PrincipalType'])),
            ('value', self.gf('django.db.models.fields.TextField')(max_length=1000)),
        ))
        db.send_create_signal(u'roster', ['SecurityPrincipal'])


    def backwards(self, orm):
        # Deleting model 'BuddyType'
        db.delete_table(u'roster_buddytype')

        # Deleting model 'Attachment'
        db.delete_table(u'roster_attachment')

        # Deleting model 'Buddy'
        db.delete_table(u'roster_buddy')

        # Removing M2M table for field attachments on 'Buddy'
        db.delete_table('roster_buddy_attachments')

        # Deleting model 'BuddyEventType'
        db.delete_table(u'roster_buddyeventtype')

        # Deleting model 'BuddyEvent'
        db.delete_table(u'roster_buddyevent')

        # Removing M2M table for field attachments on 'BuddyEvent'
        db.delete_table('roster_buddyevent_attachments')

        # Deleting model 'PrincipalType'
        db.delete_table(u'roster_principaltype')

        # Deleting model 'SecurityPrincipal'
        db.delete_table(u'roster_securityprincipal')


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
        }
    }

    complete_apps = ['roster']