# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile, CalculatedAnswer
from django.contrib.auth.models import User

import sys
import random, copy
from pprint import pprint
import xlrd
from unidecode import unidecode
# from Collections import sorted

def return_None(x):
    if x == '':
      return 0.0
    else:
      return x
      
def main(options):
    wb = xlrd.open_workbook(sys.argv[2])
    sh = wb.sheet_by_index(3)

    # CalculatedAnswer.objects.all().delete()
    # return

    for row in range(2, sh.nrows):
        vpisna = int(sh.cell_value(row, 0))
        ime = sh.cell_value(row,2)

        var1_code = sh.cell_value(row, 3)
        var2_code = sh.cell_value(row, 5)

        var1 = Dataset.objects.get(varname=var1_code)
        var2 = Dataset.objects.get(varname=var2_code)

        user = User.objects.get(username=str(vpisna))
        profile = user.get_profile()

        # if profile.is_special and str(profile.var1.sel) == '3, 6, 9, 12, 13, 17, 18, 21, 23, 24':
        #     continue

        # print row, profile.is_special, vpisna, profile.var1.sel, var1_code

        # if User.objects.filter(username=str(vpisna)).exists():
        #     user = User.objects.get(username=str(vpisna))
        #     profile = user.get_profile()
        #     profile.is_special = True
        #     profile.save()
        # else:
        #     user = User.objects.create_user(vpisna, 'none@example.com', ime.lower())
        #     profil = UserProfile(user=user, vpisna=vpisna, studijsko_leto='', izvajalec='',
        #                nacin_studija=0, cikel='', var1=var1, var2=var2, is_special=True)
        #     profil.save()

        # var1.sel = '3, 6, 9, 12, 13, 17, 18, 21, 23, 24'
        # var1.save()
        # var1.sel = '3, 6, 9, 12, 13, 17, 18, 21, 23, 24'
        # var2.save()

        for q_id, val_no in [[12,7],[13,8],[14,9], [19,10], [20,11], [62, 12], [63,13], [51,14]]:
            q = Question.objects.get(pk=q_id)
            val = float(sh.cell_value(row, val_no))
            # CalculatedAnswer.objects.get_or_create(var1=var1, var2=var2, question=q, value=val)
            try:
                calc = CalculatedAnswer.objects.get(var1=var1, var2=var2, question=q)
                delta = abs(calc.value - val)
                if delta > 0.01:
                    print '%s   Changing value from %.4f to %.4f' % (vpisna, calc.value, val)
                    # calc.value = val
                    # calc.save()
            except CalculatedAnswer.DoesNotExist:
                # CalculatedAnswer.objects.get_or_create(var1=var1, var2=var2, question=q, value=val)
                print '%s   Changing old value: %s to %s' % (vpisna, q_id, val_no)

        #     print q
        
    

class Command(BaseCommand):
    help = "imports special users that use SPSS to calculate stuff"

    def handle(self, *args, **options):
      main(options)
