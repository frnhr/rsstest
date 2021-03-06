# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Word', fields ['word']
        db.create_index(u'api_word', ['word'])

        # Adding unique constraint on 'Word', fields ['word']
        db.create_unique(u'api_word', ['word'])


    def backwards(self, orm):
        # Removing unique constraint on 'Word', fields ['word']
        db.delete_unique(u'api_word', ['word'])

        # Removing index on 'Word', fields ['word']
        db.delete_index(u'api_word', ['word'])


    models = {
        u'api.entry': {
            'Meta': {'object_name': 'Entry'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['api.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'ordering': "['word']", 'object_name': 'Word'},
            'entry': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.Entry']", 'through': u"orm['api.WordCount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'api.wordcount': {
            'Meta': {'object_name': 'WordCount'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Word']"})
        }
    }

    complete_apps = ['api']