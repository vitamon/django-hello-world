# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestsLog'
        db.create_table('request_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('hello', ['RequestsLog'])


    def backwards(self, orm):
        # Deleting model 'RequestsLog'
        db.delete_table('request_log')


    models = {
        'hello.requestslog': {
            'Meta': {'object_name': 'RequestsLog', 'db_table': "'request_log'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['hello']