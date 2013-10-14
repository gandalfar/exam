# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UserProfile.nacin_studija'
        db.alter_column('calc_userprofile', 'nacin_studija', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'UserProfile.nacin_studija'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.nacin_studija' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'UserProfile.nacin_studija'
        db.alter_column('calc_userprofile', 'nacin_studija', self.gf('django.db.models.fields.IntegerField')())

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
        'calc.answer': {
            'Meta': {'object_name': 'Answer'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calc.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'calc.calculatedanswer': {
            'Meta': {'object_name': 'CalculatedAnswer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['calc.Question']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'var1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calculated_var1'", 'to': "orm['calc.Dataset']"}),
            'var2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calculated_var2'", 'to': "orm['calc.Dataset']"})
        },
        'calc.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namee': ('django.db.models.fields.TextField', [], {}),
            'names': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'calc.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'c1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c10': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c11': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c12': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c13': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c14': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c15': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c16': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c17': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c18': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c19': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c20': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c21': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c22': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c23': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c24': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c25': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c26': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c27': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c28': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c6': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c7': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c8': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'c9': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'd1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'd2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'd3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'd4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'desce': ('django.db.models.fields.TextField', [], {}),
            'descs': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'u1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'u2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'u3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'u4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'varname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'calc.examlogentry': {
            'Meta': {'object_name': 'ExamLogEntry'},
            'commited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loggedquestion'", 'to': "orm['calc.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['auth.User']"})
        },
        'calc.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'calc.question': {
            'Meta': {'object_name': 'Question'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calc.Task']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'validator': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'visible_to': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'calc.section': {
            'Meta': {'object_name': 'Section'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calc.Lecture']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'calc.task': {
            'Meta': {'object_name': 'Task'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calc.Section']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible_to': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'calc.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'cikel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'izvajalec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'nacin_studija': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status_studenta': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'studijsko_leto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'var1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userprofile_var1'", 'to': "orm['calc.Dataset']"}),
            'var2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userprofile_var2'", 'to': "orm['calc.Dataset']"}),
            'vpisna': ('django.db.models.fields.IntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['calc']