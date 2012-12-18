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

    for row in range(2, 39):
        vpisna = int(sh.cell_value(row, 0))
        ime = sh.cell_value(row,2)

        var1_code = sh.cell_value(row, 3)
        var2_code = sh.cell_value(row, 5)

        var1 = Dataset.objects.get(varname=var1_code)
        var2 = Dataset.objects.get(varname=var2_code)

        if User.objects.filter(username=str(vpisna)).exists():
            user = User.objects.get(username=str(vpisna))
            profile = user.get_profile()
            profile.is_special = True
            profile.save()
        else:
            user = User.objects.create_user(vpisna, 'none@example.com', ime.lower())
            profil = UserProfile(user=user, vpisna=vpisna, studijsko_leto='', izvajalec='',
                       nacin_studija=0, cikel='', var1=var1, var2=var2)
            profil.save()

        var1.sel = '3,6,9,12,13,17,18,21,23,24'
        var1.save()
        var2.sel = '3,6,9,12,13,17,18,21,23,24'
        var2.save()

    #     ime = sh.cell_value(row, 2)
    #     passwd = ime.lower()
    #     passwd = unidecode(passwd)

    #     priimek = sh.cell_value(row, 1)
    #     vpisna = str(int(sh.cell_value(row, 0)))

    #     if User.objects.filter(username__exact=vpisna):
    #       print "Uporabnik %s ze obstaja v bazi" % vpisna
    #       user = User.objects.get(username__exact=vpisna)
    #       user.set_password(passwd)
    #     else:
    #       user = User.objects.create_user(vpisna, 'none@example.com', passwd)
        
    #     user.is_active = True
    #     user.first_name = ime
    #     user.last_name  = priimek
    #     user.save()
        
    #     studijsko_leto = sh.cell_value(row,7)
    #     izvajalec = sh.cell_value(row,6)

    #     raw_tip_studija = sh.cell_value(row,3)

    #     if raw_tip_studija == 'redni':
    #         nacin_studija = 0
    #     elif raw_tip_studija == 'izredni':
    #         nacin_studija = 1
    #     elif raw_tip_studija == 'Stari program':
    #         nacin_studija = 2
    #     else:
    #         nacin_studija = 3

    #     var1 = sh.cell_value(row, 8)
    #     year1 = sh.cell_value(row,9)

    #     var2 = sh.cell_value(row,10)
    #     year2 = sh.cell_value(row,11)

    #     var1 = Dataset.objects.get(year__exact=year1, varname__exact=var1)
    #     var2 = Dataset.objects.get(year__exact=year2, varname__exact=var2)
        
    #     profil = UserProfile(user=user, vpisna=vpisna, studijsko_leto=studijsko_leto, izvajalec=izvajalec,
    #                nacin_studija=nacin_studija, cikel='', var1=var1, var2=var2)
    #     profil.save()
    

class Command(BaseCommand):
    help = "imports special users that use SPSS to calculate stuff"

    def handle(self, *args, **options):
      main(options)
