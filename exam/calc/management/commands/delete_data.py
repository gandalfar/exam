# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exam.calc.models import Dataset

class Command(BaseCommand):
    help = "deletes datasets that doesnt have users associated with it"

    def handle(self, *args, **options):
        for dataset in Dataset.objects.all():
			if not bool(dataset.userprofile_var1.count() or dataset.userprofile_var2.count()):
				dataset.delete()