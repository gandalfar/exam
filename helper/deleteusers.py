import sys
import os
import random, copy
from re import escape

sys.path.append('/home/gandalf/django_exam/0910/')
sys.path.append('/home/gandalf/django_exam/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'exam.settings'
from django.contrib.auth.models import User
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile

print User.objects.filter(is_staff=False).count()
User.objects.filter(is_staff=False).delete()
print User.objects.filter(is_staff=False).count()


print User.objects.filter(is_staff=True).count()

print Dataset.objects.all().count()
Dataset.objects.all().delete()
print Dataset.objects.all().count()
