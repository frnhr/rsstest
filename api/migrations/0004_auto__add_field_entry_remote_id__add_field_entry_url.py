# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.remote_id'
        db.add_column(u'api_entry', 'remote_id',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=1000, blank=True),
                      keep_default=False)

        # Adding field 'Entry.url'
        db.add_column(u'api_entry', 'url',
                      self.gf('django.db.models.fields.URLField')(default=u'', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.remote_id'
        db.delete_column(u'api_entry', 'remote_id')

        # Deleting field 'Entry.url'
        db.delete_column(u'api_entry', 'url')


    models = {
        u'api.entry': {
            'Meta': {'object_name': 'Entry'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['api.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '1000', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '1000', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '200'})
        },
        u'api.feed': {
            'Meta': {'ordering': "['id']", 'object_name': 'Feed'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'api.word': {
            'Meta': {'object_name': 'Word'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'words'", 'to': u"orm['api.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['api']