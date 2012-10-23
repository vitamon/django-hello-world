import os
import datetime
from django.core.urlresolvers import reverse

from django.test import TestCase, Client
from requests.models import RequestsPriority, RequestsLog


class SimpleTest(TestCase):
    def test_requests(self):
        """
        test requests page
        """
        client = Client()
        response = client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Top 10 requests')

# --------------------------------------------------------------
#
# Models tests
#
# --------------------------------------------------------------
class RequestsLogTest(TestCase):
    def test_add_item(self):
        """
        test middleware to save requests in RequestsLog
        """
        client = Client()
        try:
            response = client.get(os.path.join(reverse('home'), "blabla"))
        except:
            pass
        last_req_item = RequestsLog.objects.get_last_n(1)[0]
        assert "blabla" in last_req_item.url

    def test_sorted(self):
        RequestsPriority.objects.create(url="http://rr.com", priority=-3)
        RequestsPriority.objects.create(url="http://yahoo.com", priority=3)
        RequestsPriority.objects.create(url="http://ya.com", priority=5)
        RequestsLog.objects.create(url="http://rr.com", time=datetime.datetime.now())
        RequestsLog.objects.create(url="http://yahoo.com", time=datetime.datetime.now())
        RequestsLog.objects.create(url="http://ya.com", time=datetime.datetime.now())
        RequestsLog.objects.create(url="http://bababa.com", time=datetime.datetime.now())
        lst = RequestsLog.objects.get_last_10_sorted()
        assert lst[0]['priority'] == 5
        #print RequestsLog.objects.get_last_10_sorted()


class RequestPriorityModelTest(TestCase):
    def test_non_existing(self):
        assert RequestsPriority.objects.lookup("anything") == RequestsPriority.objects.DEFAULT_PRIORITY

    def test_lookup(self):
        RequestsPriority.objects.create(url="http://yahoo.com", priority=3)
        assert RequestsPriority.objects.lookup("http://yahoo.com") == 3

