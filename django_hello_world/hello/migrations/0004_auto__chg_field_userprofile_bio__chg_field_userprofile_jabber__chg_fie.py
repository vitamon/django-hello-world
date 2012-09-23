# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UserProfile.bio'
        db.alter_column('hello_userprofile', 'bio', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'UserProfile.jabber'
        db.alter_column('hello_userprofile', 'jabber', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'UserProfile.photo'
        db.alter_column('hello_userprofile', 'photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'UserProfile.skype'
        db.alter_column('hello_userprofile', 'skype', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'UserProfile.other_contacts'
        db.alter_column('hello_userprofile', 'other_contacts', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

    def backwards(self, orm):

        # Changing field 'UserProfile.bio'
        db.alter_column('hello_userprofile', 'bio', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'UserProfile.jabber'
        db.alter_column('hello_userprofile', 'jabber', self.gf('django.db.models.fields.CharField')(max_length=20))

        # User chose to not deal with backwards NULL issues for 'UserProfile.photo'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.photo' and its values cannot be restored.")

        # Changing field 'UserProfile.skype'
        db.alter_column('hello_userprofile', 'skype', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'UserProfile.other_contacts'
        db.alter_column('hello_userprofile', 'other_contacts', self.gf('django.db.models.fields.CharField')(max_length=250))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hello.requestslog': {
            'Meta': {'object_name': 'RequestsLog', 'db_table': "'request_log'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'hello.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'null': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True'}),
            'other_contacts': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['hello']