from unittest import TestCase
import datetime
from django.db import models


class RequestsLogManager(models.Manager):
    def get_last_ten(self):
        return self.get_last_n(10)

    def get_last_n(self,n):
        return self.order_by("-time")[:n]


class RequestsLog(models.Model):
    url = models.URLField()
    time = models.DateTimeField()
    objects = RequestsLogManager()

    class Meta:
        db_table = 'request_log'


class ModelTest(TestCase):
    def test_add_item(self):
        time = datetime.datetime.now()
        item = RequestsLog(url="test1", time=time)
        item.save()
        saved_item = RequestsLog.objects.get_last_n(1)[0]
        assert saved_item.url == item.url

