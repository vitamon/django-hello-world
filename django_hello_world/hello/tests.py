from unittest import skip
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from selenium import webdriver

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
        from context_processors import django_settings
        sets = django_settings({})
        assert 'settings' in sets
        import settings
        assert sets['settings'].ADMIN_MEDIA_PREFIX == settings.ADMIN_MEDIA_PREFIX

    def test_settings_content_processor(self):
        client = Client()
        response = client.get(reverse('home'))
        import settings
        assert settings.AUTHOR is not None
        self.assertContains(response, settings.AUTHOR)

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
        """
        browser = webdriver.Firefox()
        browser.get('http://localhost:8000/logout')
        assert 'login' in browser.page_source
        browser.find_element_by_id("login").click()
        browser.implicitly_wait(500)
        self.assertRegexpMatches(browser.current_url, r'login/$')
        browser.close()