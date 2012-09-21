from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assignment')


class BaseSeleniumTest(TestCase):
    def test_simple(self):
        from selenium import webdriver

        browser = webdriver.Firefox() # Get local session of firefox
        browser.get('http://0.0.0.0:8000') # Load page
        assert "Hello, 42cc!!!" in browser.title
        browser.close()
