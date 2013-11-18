# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from south.db import db
from south.v2 import SchemaMigration
import datetime


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ItemComment.content_html'
        db.add_column(u'lms_itemcomment', 'content_html',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Trail.created_by'
        db.delete_column(u'lms_trail', 'created_by_id')

        # Adding field 'Trail.content_html'
        db.add_column(u'lms_trail', 'content_html',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Item.created_by'
        db.delete_column(u'lms_item', 'created_by_id')

        # Adding field 'Item.content_html'
        db.add_column(u'lms_item', 'content_html',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserItem.created_at'
        db.add_column(u'lms_useritem', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True),
                      keep_default=False)

        # Adding field 'UserItem.checked_at'
        db.add_column(u'lms_useritem', 'checked_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Solution.privacy'
        db.add_column(u'lms_solution', 'privacy',
                      self.gf('django.db.models.fields.IntegerField')(default=100),
                      keep_default=False)

        # Adding field 'Solution.code'
        db.add_column(u'lms_solution', 'code',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Solution.content_html'
        db.add_column(u'lms_solution', 'content_html',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Solution.content'
        db.alter_column(u'lms_solution', 'content', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Deleting field 'ItemComment.content_html'
        db.delete_column(u'lms_itemcomment', 'content_html')


        # User chose to not deal with backwards NULL issues for 'Trail.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Trail.created_by' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Trail.created_by'
        db.add_column(u'lms_trail', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='trails', to=orm['users.HackitaUser']),
                      keep_default=False)

        # Deleting field 'Trail.content_html'
        db.delete_column(u'lms_trail', 'content_html')


        # User chose to not deal with backwards NULL issues for 'Item.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Item.created_by' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.created_by'
        db.add_column(u'lms_item', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='lms_items', to=orm['users.HackitaUser']),
                      keep_default=False)

        # Deleting field 'Item.content_html'
        db.delete_column(u'lms_item', 'content_html')

        # Deleting field 'UserItem.created_at'
        db.delete_column(u'lms_useritem', 'created_at')

        # Deleting field 'UserItem.checked_at'
        db.delete_column(u'lms_useritem', 'checked_at')

        # Deleting field 'Solution.privacy'
        db.delete_column(u'lms_solution', 'privacy')

        # Deleting field 'Solution.code'
        db.delete_column(u'lms_solution', 'code')

        # Deleting field 'Solution.content_html'
        db.delete_column(u'lms_solution', 'content_html')


        # User chose to not deal with backwards NULL issues for 'Solution.content'
        raise RuntimeError("Cannot reverse this migration. 'Solution.content' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Solution.content'
        db.alter_column(u'lms_solution', 'content', self.gf('django.db.models.fields.TextField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lms.item': {
            'Meta': {'ordering': "('ordinal',)", 'object_name': 'Item'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exercise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['lms.Trail']"})
        },
        u'lms.itemcomment': {
            'Meta': {'object_name': 'ItemComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['users.HackitaUser']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['lms.Item']"})
        },
        u'lms.solution': {
            'Meta': {'object_name': 'Solution'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solutions'", 'to': u"orm['users.HackitaUser']"}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solutions'", 'to': u"orm['lms.Item']"}),
            'privacy': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        u'lms.trail': {
            'Meta': {'ordering': "('ordinal',)", 'object_name': 'Trail'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'lms.useritem': {
            'Meta': {'object_name': 'UserItem'},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mentor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lms.Item']"}),
            'liked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.HackitaUser']"})
        },
        u'users.hackitauser': {
            'Meta': {'object_name': 'HackitaUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'english_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'english_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'forms_filled': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'hebrew_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hebrew_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_form_filled': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['lms']