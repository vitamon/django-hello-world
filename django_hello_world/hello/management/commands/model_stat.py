# -*- coding: utf-8 -*-
import sys
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    """
    Prints list of all models and objects count

    To execute the command and save output of stderr into file
    with file name to be current date with extension .dat:

    run_model_stat.sh :
        now=$(date +"%m_%d_%Y")
        python manage.py model_stat 2> $now.dat

    """

    def out(self, value):
        print value
        sys.stderr.write(u'error: %s\n' % value)

    def handle(self, *args, **options):
        for ct in ContentType.objects.all():
            m = ct.model_class()
            self.out(u"%s.%s : %d" % (m.__module__, m.__name__, m._default_manager.count()))
        return