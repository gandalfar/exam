import sys
import os
import random, copy
from re import escape

sys.path.append('/home/gandalf/statistika/0607/')
sys.path.append('/Users/gandalf/django/django_exam/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'exam.settings'
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile
from django.contrib.auth.models import User

from exam.calc.validators.statistika import seznam_vzorec

answer_list = Answer.objects.filter(question__task__exact=8, correct=True)

print answer_list.count()

for a in answer_list:
	a.correct = False
	a.save()
