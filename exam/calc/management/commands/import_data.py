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
      return None
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
        print line

        args = {"region":line[0],
                "varname":line[1],
                "year":int(line[2]),
                "descs":line[3],
                "desce":line[5],
                "c1":return_None(line[8]),
                "c2":return_None(line[9]),
                "c3":return_None(line[10]),
                "c4":return_None(line[11]),
                "c5":return_None(line[12]),
                "c6":return_None(line[13]),
                "c7":return_None(line[14]),
                "c8":return_None(line[15]),
                "c9":return_None(line[16]),
                "c10":return_None(line[17]),
                "c11":return_None(line[18]),
                "c12":return_None(line[19]),
                "c13":return_None(line[20]),
                "c14":return_None(line[21]),
                "c15":return_None(line[22]),
                "c16":return_None(line[23]),
                "c17":return_None(line[24]),
                "c18":return_None(line[25]),
                "c19":return_None(line[26]),
                "c20":return_None(line[27]),
                "c21":return_None(line[28]),
                "c22":return_None(line[29]),
                "c23":return_None(line[30]),
                "c24":return_None(line[31]),
                "c25":return_None(line[32]),
                "c26":return_None(line[33]),
                "c27":return_None(line[34]),
                "c28":return_None(line[35]),
                # "d1": check_index(line, 36),
                # "u1": check_index(line, 37),
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
        p.save()
        p.generate_sample()

class Command(BaseCommand):
    help = "imports data in csv, tab delimited format"

    def handle(self, *args, **options):
        main(options)
