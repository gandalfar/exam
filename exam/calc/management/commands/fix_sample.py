# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exam.calc.models import Lecture, Task, Section, Question, Answer, ExamLogEntry, Dataset, UserProfile, CalculatedAnswer
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "fixes country sample for 2013/14 year"

    def handle(self, *args, **options):
        # for var in Dataset.objects.all():
        #     if var.varname in ['GEB1.2001', 'GEB1.2001-AS', 'PS25.2001', 'PS25.2001-AS']:
        #         continue

        #     if not var.userprofile_var1.count():
        #         continue

        #     # print var.userprofile_var1.all()
            
        #     sample = [int(i) for i in var.sel.split(',')]
        #     sample.sort()
        #     orig_sample = sample

        #     sample = list(set(sample))
        #     full_sample_count = len(var.get_sample_values())

        #     if (len(sample) != 10) or (25 not in sample) or (full_sample_count != 10):
        #         for vpisna in var.userprofile_var1.all():
        #             print '\t',vpisna

        #         var.generate_sample()
        #     # print sample

        for var in Dataset.objects.filter(varname__endswith='-AS'):
          if var.varname in ['GEB1.2001', 'GEB1.2001-AS', 'PS25.2001', 'PS25.2001-AS']:
              continue

          print var.varname

          var.sel = '3, 6, 9, 13, 14, 18, 19, 22, 24, 25'
          var.save()