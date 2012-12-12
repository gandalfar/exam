# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile
from django.contrib.auth.models import User

import sys
import random, copy
from pprint import pprint
import xlrd

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

def main(options):
    wb = xlrd.open_workbook(sys.argv[2])
    sh = wb.sheet_by_index(0)

    for row in range(1, sh.nrows):
        line = sh.row_values(row)
        
        args = {"region":line[0],
                "varname":line[1],
                "year":int(line[2]),
                "descs":line[3],
                "desce":line[5],
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
                "c26":return_None(line[32]),
                "c27":return_None(line[33]),
                "d1": check_index(line, 34),
                "u1": check_index(line, 35),
                }

        dataset_args = {}

        for i in args:
          if args[i]:
            dataset_args[i] = args[i]

        if Dataset.objects.filter(varname=args['varname'], year=args['year']).count():
            p = Dataset.objects.get(varname=args['varname'], year=args['year'])
        else:
            p = Dataset(**args)

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

        p.save()

class Command(BaseCommand):
    help = "imports data in csv, tab delimited format"

    def handle(self, *args, **options):
        main(options)
