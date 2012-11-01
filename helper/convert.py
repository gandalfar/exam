# -*- coding: utf-8 -*-
import sys
import os
import random, copy
from re import escape

sys.path.append('/home/gandalf/statistika/0809/')
sys.path.append('/Users/gandalf/django/django_exam/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'exam.settings'
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile
from django.contrib.auth.models import User

def return_None(x):
    if x == '':
      return 0.0
    else:
      return x

'''
f = open('podatki09.csv')
for line in f.readlines():
    line = line.replace('"', '')
    line = line.replace('\n','')
    line = line.split('\t')
    
    
    args = {"region":line[1], 
            "varname":line[2],
            "desce":line[3],
            "descs":line[4],
            "u1":line[5].encode('utf-8'),
            "year":line[6],
            "c1":return_None(line[7]),
            "c2":return_None(line[8]),
            "c3":return_None(line[9]),
            "c4":return_None(line[10]),                                    
            "c5":return_None(line[11]),
            "c6":return_None(line[12]),
            "c7":return_None(line[13]),
            "c8":return_None(line[14]),
            "c9":return_None(line[15]),                                    
            "c10":return_None(line[16]),
            "c11":return_None(line[17]),
            "c12":return_None(line[18]),
            "c13":return_None(line[19]),
            "c14":return_None(line[20]),                                    
            "c15":return_None(line[21]),
            "c16":return_None(line[22]),
            "c17":return_None(line[23]),
            "c18":return_None(line[24]),
            "c19":return_None(line[25]),                                    
            "c20":return_None(line[26]),
            "c21":return_None(line[27]),
            "c22":return_None(line[28]),
            "c23":return_None(line[29]),
            "c24":return_None(line[30]),                                    
            "c25":return_None(line[31]),
            }
            
    dataset_args = {}
    
    for i in args:
      if args[i]:
        dataset_args[i] = args[i]
    
    if Dataset.objects.filter(varname=line[2], year=line[6]).count():
      p = Dataset.objects.get(varname=line[2], year=line[6])
    else:
      p = Dataset(**args)
      
    print p
          
    # note the missing 21 because we include it everytime
    #seznam = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25]
    
    old_member = [1,3,4,6,7,8,9,10,14,17,18,20,23,24,25]
    new_member = [2,5,11,12,13,15,16,19,22]
    picked = [21]
    
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
            
    s = str(picked).strip('[]')
    p.sel = s
    p.save()
    print p
'''

#'''
f = open('letni09.csv')
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
    
    print line[8], line[7]
    print [line]
  
    var1 = Dataset.objects.get(year__exact=int(line[8]), varname__exact=line[7])
    var2 = Dataset.objects.get(year__exact=int(line[10]), varname__exact=line[9])
  
    profil = UserProfile(user=user, vpisna=vpisna, studijsko_leto=studijsko_leto, izvajalec=izvajalec,
               nacin_studija=nacin_studija, cikel=cikel, var1=var1, var2=var2)
    profil.save()
  	#print [vpisna, studijsko_leto, status_studenta, izvajalec, nacin_studija, cikel, var1, var2]
#'''
f.close()
