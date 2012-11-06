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
        db.send_create_signal('requests', ['RequestsLog'])

        # Adding model 'RequestsPriority'
        db.create_table('hello_request_priority', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('priority', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('requests', ['RequestsPriority'])


    def backwards(self, orm):
        # Deleting model 'RequestsLog'
        db.delete_table('request_log')

        # Deleting model 'RequestsPriority'
        db.delete_table('hello_request_priority')


    models = {
        'requests.requestslog': {
            'Meta': {'object_name': 'RequestsLog', 'db_table': "'request_log'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'requests.requestspriority': {
            'Meta': {'object_name': 'RequestsPriority', 'db_table': "'hello_request_priority'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['requests']