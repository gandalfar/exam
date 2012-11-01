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

f = open('student.1112.csv')
for line in f.readlines():
    line = line.replace(' "', '"')
    line = line.replace('"', '')
    line = line.replace('\n','')
    line = line.split('\t')

    passwd = line[2].lower()
    passwd = passwd.replace('\xc5\xa1', 's')
    passwd = passwd.replace('\xc5\xbe', 'z')
    #neki cudni krogci so prisli v podatke
    passwd = passwd.replace('\xc2\xa0', '')
    #Z -> z
    passwd = passwd.replace('\xc5\xbd', 'z')
    #S -> s
    passwd = passwd.replace('\xc5\xa0', 's')
    #C -> c
    passwd = passwd.replace('\xc4\x8c', 'c')

    print "Geslo:", [passwd]

    ime = line[2]
    ime = ime.replace('\xc2\xa0', '')

    priimek = line[1]
    priimek = priimek.replace('\xc2\xa0', '')

    vpisna = line[0]
    vpisna = vpisna.replace('\xc2\xa0', '')

    if User.objects.filter(username__exact=vpisna):
      print "Uporabnik %s ze obstaja v bazi" % vpisna
      continue
      user = User.objects.get(username__exact=vpisna)
      user.set_password(passwd)
    else:
      user = User.objects.create_user(vpisna, 'none@example.com', passwd)

    print user

    user.is_staff = False
    user.is_superuser = False
    user.is_active = True
    user.first_name = ime
    user.last_name  = priimek
    user.save()


    #status_studenta = line[3]
    studijsko_leto = line[3]
    izvajalec = line[4]

    raw_tip_studija = line[5]
    raw_tip_studija = raw_tip_studija.replace('\xc2\xa0', '')

    if raw_tip_studija == 'redni':
      nacin_studija = 0
    elif raw_tip_studija == 'izredni':
      nacin_studija = 1
    elif raw_tip_studija == 'Stari program':
      nacin_studija = 2
    else:
      nacin_studija = 3

    cikel = line[6]
    cikel = cikel.replace('\xc5\xa0', 'S')

    print line[11], line[8], line[12]
    print [line]

    var1 = Dataset.objects.get(year__exact=int(line[9]), varname__exact=line[12])
    var2 = Dataset.objects.get(year__exact=int(line[11]), varname__exact=line[13])

    profil = UserProfile(user=user, vpisna=vpisna, studijsko_leto=studijsko_leto, izvajalec=izvajalec,
               nacin_studija=nacin_studija, cikel=cikel, var1=var1, var2=var2)
    profil.save()
