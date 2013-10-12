# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile
from django.contrib.auth.models import User

import sys
import random, copy
from pprint import pprint
import xlrd
from unidecode import unidecode

def return_None(x):
    if x == '':
      return 0.0
    else:
      return x
      
def main(options):
    wb = xlrd.open_workbook(sys.argv[2])
    sh = wb.sheet_by_index(0)

    User.objects.filter(is_superuser=False).delete()

    for row in range(1, sh.nrows):
        ime = sh.cell_value(row, 2)
        passwd = ime.lower()
        passwd = unidecode(passwd)

        priimek = sh.cell_value(row, 1)
        vpisna = str(int(sh.cell_value(row, 0)))

        print row, vpisna

        if User.objects.filter(username__exact=vpisna):
          print "Uporabnik %s ze obstaja v bazi" % vpisna
          user = User.objects.get(username__exact=vpisna)
          user.set_password(passwd)
        else:
          user = User.objects.create_user(vpisna, 'none@example.com', passwd)
        
        user.is_active = True
        user.first_name = ime
        user.last_name  = priimek
        user.save()
        
        studijsko_leto = sh.cell_value(row,7)
        izvajalec = sh.cell_value(row,6)

        raw_tip_studija = sh.cell_value(row,3)

        if raw_tip_studija == 'redni':
            nacin_studija = 0
        elif raw_tip_studija == 'izredni':
            nacin_studija = 1
        elif raw_tip_studija == 'Stari program':
            nacin_studija = 2
        else:
            nacin_studija = 3

        var1 = sh.cell_value(row, 8)
        year1 = sh.cell_value(row,9)

        var2 = sh.cell_value(row,10)
        year2 = sh.cell_value(row,11)

        var1 = Dataset.objects.get(varname__exact=var1)
        var2 = Dataset.objects.get(varname__exact=var2)
        

        UserProfile.objects.get_or_create(
            user = user,
            vpisna = vpisna,
            defaults = {
                'studijsko_leto': studijsko_leto, 
                'izvajalec': izvajalec,
                'nacin_studija': nacin_studija, 
                'cikel': '', 
                'var1': var1, 
                'var2': var2            
            }
        )    

class Command(BaseCommand):
    help = "imports users in csv, tab delimited format"

    def handle(self, *args, **options):
      main(options)
