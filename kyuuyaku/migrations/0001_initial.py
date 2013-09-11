# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Char'
        db.create_table(u'kyuuyaku_char', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('printable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'kyuuyaku', ['Char'])

        # Adding model 'CharBlock'
        db.create_table(u'kyuuyaku_charblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal(u'kyuuyaku', ['CharBlock'])

        # Adding model 'CharBlockChar'
        db.create_table(u'kyuuyaku_charblockchar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kyuuyaku.CharBlock'])),
            ('char', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kyuuyaku.Char'])),
            ('location', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'kyuuyaku', ['CharBlockChar'])

        # Adding unique constraint on 'CharBlockChar', fields ['block', 'location']
        db.create_unique(u'kyuuyaku_charblockchar', ['block_id', 'location'])

        # Adding model 'CharBlockOCR'
        db.create_table(u'kyuuyaku_charblockocr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kyuuyaku.CharBlock'])),
            ('segment', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'kyuuyaku', ['CharBlockOCR'])

        # Adding unique constraint on 'CharBlockOCR', fields ['block', 'segment']
        db.create_unique(u'kyuuyaku_charblockocr', ['block_id', 'segment'])

        # Adding model 'Message'
        db.create_table(u'kyuuyaku_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pointer', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'kyuuyaku', ['Message'])

        # Adding model 'CharVote'
        db.create_table(u'kyuuyaku_charvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IntegerField')()),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('char', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kyuuyaku.Char'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal(u'kyuuyaku', ['CharVote'])

        # Adding model 'MessageVote'
        db.create_table(u'kyuuyaku_messagevote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IntegerField')()),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kyuuyaku.Message'])),
            ('translation', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'kyuuyaku', ['MessageVote'])


    def backwards(self, orm):
        # Removing unique constraint on 'CharBlockOCR', fields ['block', 'segment']
        db.delete_unique(u'kyuuyaku_charblockocr', ['block_id', 'segment'])

        # Removing unique constraint on 'CharBlockChar', fields ['block', 'location']
        db.delete_unique(u'kyuuyaku_charblockchar', ['block_id', 'location'])

        # Deleting model 'Char'
        db.delete_table(u'kyuuyaku_char')

        # Deleting model 'CharBlock'
        db.delete_table(u'kyuuyaku_charblock')

        # Deleting model 'CharBlockChar'
        db.delete_table(u'kyuuyaku_charblockchar')

        # Deleting model 'CharBlockOCR'
        db.delete_table(u'kyuuyaku_charblockocr')

        # Deleting model 'Message'
        db.delete_table(u'kyuuyaku_message')

        # Deleting model 'CharVote'
        db.delete_table(u'kyuuyaku_charvote')

        # Deleting model 'MessageVote'
        db.delete_table(u'kyuuyaku_messagevote')


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
            'image_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
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