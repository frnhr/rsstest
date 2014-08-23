# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WordCount'
        db.create_table(u'api_wordcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Word'])),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Entry'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'api', ['WordCount'])

        # Deleting field 'Word.count'
        db.delete_column(u'api_word', 'count')

        # Deleting field 'Word.entry'
        db.delete_column(u'api_word', 'entry_id')


    def backwards(self, orm):
        # Deleting model 'WordCount'
        db.delete_table(u'api_wordcount')

        # Adding field 'Word.count'
        db.add_column(u'api_word', 'count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Word.entry'
        raise RuntimeError("Cannot reverse this migration. 'Word.entry' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Word.entry'
        db.add_column(u'api_word', 'entry',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='words', to=orm['api.Entry']),
                      keep_default=False)


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
            'Meta': {'ordering': "['word', 'entry__id']", 'object_name': 'Word'},
            'entry': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.Entry']", 'through': u"orm['api.WordCount']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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