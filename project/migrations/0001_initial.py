# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteResource'
        db.create_table(u'project_siteresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal(u'project', ['SiteResource'])


    def backwards(self, orm):
        # Deleting model 'SiteResource'
        db.delete_table(u'project_siteresource')


    models = {
        u'project.siteresource': {
            'Meta': {'ordering': "['name']", 'object_name': 'SiteResource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('tinymce.models.HTMLField', [], {})
        }
    }

    complete_apps = ['project']