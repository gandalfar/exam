# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

def main(options):
    print User.objects.filter(is_staff=False).count()
    User.objects.filter(is_staff=False).delete()

class Command(BaseCommand):
    help = "Delete non-admin users"
    args = ''

    def handle(self, *args, **options):
      main(options)
