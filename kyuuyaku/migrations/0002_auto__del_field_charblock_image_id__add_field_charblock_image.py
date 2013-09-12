# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CharBlock.image_id'
        db.delete_column(u'kyuuyaku_charblock', 'image_id')

        # Adding field 'CharBlock.image'
        db.add_column(u'kyuuyaku_charblock', 'image',
                      self.gf('django.db.models.fields.TextField')(unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'CharBlock.image_id'
        db.add_column(u'kyuuyaku_charblock', 'image_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0, unique=True),
                      keep_default=False)

        # Deleting field 'CharBlock.image'
        db.delete_column(u'kyuuyaku_charblock', 'image')


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
            'Meta': {'unique_together': "[('block', 'location')]", 'object_name': 'CharBlockChar'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.CharBlock']"}),
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Char']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.IntegerField', [], {})
        },
        u'kyuuyaku.charblockocr': {
            'Meta': {'unique_together': "[('block', 'segment')]", 'object_name': 'CharBlockOCR'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.CharBlock']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'segment': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'kyuuyaku.charvote': {
            'Meta': {'object_name': 'CharVote'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Char']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IntegerField', [], {}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'Meta': {'object_name': 'MessageVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IntegerField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kyuuyaku.Message']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'translation': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['kyuuyaku']