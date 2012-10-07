import os
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from hello.models import RequestsLog
from selenium import webdriver
from context_processors import django_settings
import settings

class HttpTest(TestCase):
    def test_home(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assignment')

    def test_requests(self):
        """
        test requests page
        """
        client = Client()
        response = client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Top 10 requests')

    def test_context_processor(self):
        sets = django_settings({})
        assert 'settings' in sets
        assert sets['settings'].ADMIN_MEDIA_PREFIX == settings.ADMIN_MEDIA_PREFIX

    def test_settings_content_processor(self):
        """
        check if author metadata is filled in the template from settings
        """
        client = Client()
        response = client.get(reverse('home'))
        assert settings.AUTHOR is not None
        self.assertContains(response, settings.AUTHOR)

# --------------------------------------------------------------
#
# Models tests
#
# --------------------------------------------------------------
class ModelTest(TestCase):
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


# --------------------------------------------------------------
#
# Selenium tests
#
# --------------------------------------------------------------

class SeleniumTests(TestCase):
    def test_selenium_simple(self):
        browser = webdriver.Firefox() # Get local session of firefox
        browser.get('http://localhost:8000') # Load page
        assert "Hello, 42cc!" in browser.title
        browser.close()

    def test_click_request(self):
        """
        opens the homepage, clicks requests link,
        should be open the requests page
        """
        browser = webdriver.Firefox()
        browser.get('http://localhost:8000')
        browser.find_element_by_id(r"req_link").click()
        browser.implicitly_wait(500)
        self.assertRegexpMatches(browser.current_url, r'requests/$')
        assert 'Top 10 requests' in browser.page_source
        browser.close()

    def test_login(self):
        """
        logout, press Edit, check we are on login page
        """
        browser = webdriver.Firefox()
        browser.get('http://localhost:8000/logout')
        assert 'Edit' in browser.page_source
        browser.find_element_by_id("login").click()
        browser.implicitly_wait(500)
        self.assertRegexpMatches(browser.current_url, r'login/$')
        browser.find_element_by_id()
        browser.close()