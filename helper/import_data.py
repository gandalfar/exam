# -*- coding: utf-8 -*-
import sys
import os
import random, copy
from re import escape
from pprint import pprint

# sys.path.append('/home/gandalf/statistika/0809/')
# sys.path.append('/Users/gandalf/django/django_exam/')
# sys.path.append('/home/gandalf/django_exam/0910/')
# sys.path.append('/home/gandalf/django_exam/')
sys.path.append('..')

os.environ['DJANGO_SETTINGS_MODULE'] = 'exam.settings'
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile
from django.contrib.auth.models import User

def return_None(x):
    if x == '':
      return 0.0
    else:
      return x

def check_index(x, idx):
    if len(x)-1 == idx:
      return x[idx]
    else:
      return ''

#delete all datasets, except for sample data
for dataset in Dataset.objects.all():
  if dataset.varname in ['GEB1.2001', 'PS25.2001']:
    continue
  else:
    dataset.delete()

#delete all users, except admin/sample users
for user in User.objects.all():
  try:
    print user.userprofile
  except:
    user.delete()

f = open('podatki.1112.csv')
for line in f.readlines():
    line = line.replace('"', '')
    line = line.replace('\n','')
    line = line.split('\t')

    line.insert(3, "")
    print line

    args = {"region":line[0],
            "varname":line[1],
            "desce":line[2],
            "descs":line[3],
            "year":line[4],
            "c1":return_None(line[5]),
            "c2":return_None(line[6]),
            "c3":return_None(line[7]),
            "c4":return_None(line[8]),
            "c5":return_None(line[9]),
            "c6":return_None(line[10]),
            "c7":return_None(line[11]),
            "c8":return_None(line[12]),
            "c9":return_None(line[13]),
            "c10":return_None(line[14]),
            "c11":return_None(line[15]),
            "c12":return_None(line[16]),
            "c13":return_None(line[17]),
            "c14":return_None(line[18]),
            "c15":return_None(line[19]),
            "c16":return_None(line[20]),
            "c17":return_None(line[21]),
            "c18":return_None(line[22]),
            "c19":return_None(line[23]),
            "c20":return_None(line[24]),
            "c21":return_None(line[25]),
            "c22":return_None(line[26]),
            "c23":return_None(line[27]),
            "c24":return_None(line[28]),
            "c25":return_None(line[29]),
            "c26":return_None(line[30]),
            "c27":return_None(line[31]),
            "d1": check_index(line, 33),
            "u1": check_index(line, 34),
            }

    dataset_args = {}

    for i in args:
      if args[i]:
        dataset_args[i] = args[i]

    if Dataset.objects.filter(varname=line[1], year=line[4]).count():
      p = Dataset.objects.get(varname=line[1], year=line[4])
    else:
      p = Dataset(**args)
    
    pprint(args)
    for x in args:
       setattr(p, x, args[x])

    # note the missing 24 because we include it everytime
    seznam = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27]
    

    old_member = [1,2,6,8,9,10,11,12,15,18,19,21,25,26,27]
    new_member = [3,4,5,7,13,14,16,17,20,22,23]
    picked = [24]
    
    for i in old_member:
      if getattr(p, 'c'+str(i)) == 0.0:
        old_member.remove(i)
    
    for i in new_member:
      if getattr(p, 'c'+str(i)) == 0.0:
        new_member.remove(i)
    
    for n in range(0,6):
      g = random.choice(old_member)
      old_member.remove(g)
      picked.append(g)
      print "old:", g
    
    
    for n in range(0,3):
      g = random.choice(new_member)
      new_member.remove(g)
      picked.append(g)
      print "new:", g
    
    print "picked #", len(picked)
    s = str(picked).strip('[]')
    p.sel = s
    
    print p
    p.save()
    