# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CharVote.submitted'
        db.delete_column(u'kyuuyaku_charvote', 'submitted')

        # Adding field 'CharVote.modified'
        db.add_column(u'kyuuyaku_charvote', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 9, 12, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'CharVote.ip'
        db.alter_column(u'kyuuyaku_charvote', 'ip', self.gf('django.db.models.fields.CharField')(max_length=15))
        # Adding unique constraint on 'CharVote', fields ['ip', 'char']
        db.create_unique(u'kyuuyaku_charvote', ['ip', 'char_id'])

        # Deleting field 'MessageVote.submitted'
        db.delete_column(u'kyuuyaku_messagevote', 'submitted')

        # Adding field 'MessageVote.modified'
        db.add_column(u'kyuuyaku_messagevote', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 9, 12, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'MessageVote.ip'
        db.alter_column(u'kyuuyaku_messagevote', 'ip', self.gf('django.db.models.fields.CharField')(max_length=15))
        # Adding unique constraint on 'MessageVote', fields ['ip', 'message']
        db.create_unique(u'kyuuyaku_messagevote', ['ip', 'message_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MessageVote', fields ['ip', 'message']
        db.delete_unique(u'kyuuyaku_messagevote', ['ip', 'message_id'])

        # Removing unique constraint on 'CharVote', fields ['ip', 'char']
        db.delete_unique(u'kyuuyaku_charvote', ['ip', 'char_id'])

        # Adding field 'CharVote.submitted'
        db.add_column(u'kyuuyaku_charvote', 'submitted',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 9, 12, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'CharVote.modified'
        db.delete_column(u'kyuuyaku_charvote', 'modified')


        # Changing field 'CharVote.ip'
        db.alter_column(u'kyuuyaku_charvote', 'ip', self.gf('django.db.models.fields.IntegerField')())
        # Adding field 'MessageVote.submitted'
        db.add_column(u'kyuuyaku_messagevote', 'submitted',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 9, 12, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'MessageVote.modified'
        db.delete_column(u'kyuuyaku_messagevote', 'modified')


        # Changing field 'MessageVote.ip'
        db.alter_column(u'kyuuyaku_messagevote', 'ip', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'kyuuyaku.char': {
            'Meta': {'object_name': 'Char'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        u'kyuuyaku.charblock': {
            'Meta': {'object_name': 'CharBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.TextField', [], {'unique': 'True', 'null': 'True'})
        },
        u'kyuuyaku.charblockchar': {
            'Meta': {'unique_together': "[('block', 'segment', 'location')]", 'object_name': 'CharBlockChar'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.CharBlock']"}),
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Char']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.IntegerField', [], {}),
            'segment': ('django.db.models.fields.IntegerField', [], {})
        },
        u'kyuuyaku.charblockocr': {
            'Meta': {'unique_together': "[('block', 'segment')]", 'object_name': 'CharBlockOCR'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.CharBlock']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'segment': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'kyuuyaku.charvote': {
            'Meta': {'unique_together': "[('ip', 'char')]", 'object_name': 'CharVote'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Char']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        u'kyuuyaku.message': {
            'Meta': {'object_name': 'Message'},
            'data': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pointer': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'kyuuyaku.messagevote': {
            'Meta': {'unique_together': "[('ip', 'message')]", 'object_name': 'MessageVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'translation': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['kyuuyaku']