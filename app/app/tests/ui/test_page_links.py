import pytest
import re
import requests
import unittest

from django.test import LiveServerTestCase

from app.urls import urlpatterns

from conftest import Data

@pytest.mark.skip(reason="test server required to be setup so tests work.")
class TestRenderedTemplateLinks:
    """UI Links tests """

    server_host: str = '127.0.0.1'
    # server_host: str  = '192.168.1.172'
    server_url: str = 'http://' + server_host + ':8002/'
    

    data = Data()

    driver = None
    """ Chrome webdriver """

    session = None
    """ Client session that is logged into the dejango site """


    def setup_class(self):
        """ Set up the test

        1. fetch session cookie
        2. login to site
        3. save session for use in tests
        """

        self.session = requests.Session()

        # fetch the csrf token
        self.session.get(
            url = self.server_url + 'account/login/',
        )

        # login
        self.client = self.session.post(
            url = self.server_url + 'account/login/',
            data = {
                'username': 'admin',
                'password': 'admin',
                'csrfmiddlewaretoken': self.session.cookies._cookies[self.server_host]['/']['csrftoken'].value
            }
        )



    @pytest.mark.parametrize(
        argnames='url', 
        argvalues=[link for link in data.urls], 
        ids=[link for link in data.urls]
    )
    def test_ui_no_http_forbidden(self, url):
        """ Test Page Links

        Scrape the page for links and ensure none return HTTP/403.

        Test failure denotes a link on a page that should have been filtered out by testing for user
        permissions within the template.

        Args:
            url (str): Page to test
        """

        response = self.session.get(
            url = str(self.server_url + url)
        )

        # Failsafe to ensure no redirection and that page exists
        assert len(response.history) == 0
        assert response.status_code == 200

        page_urls = []

        page = str(response.content)

        links = re.findall('href=\"([a-z\/0-9]+)\"', page)

        for link in links:

            page_link_response = self.session.get(
                url = str(self.server_url + link)
            )

            # Failsafe to ensure no redirection
            assert len(response.history) == 0

            assert page_link_response.status_code != 403



    @pytest.mark.parametrize(
        argnames='url', 
        argvalues=[link for link in data.urls], 
        ids=[link for link in data.urls]
    )
    def test_ui_no_http_not_found(self, url):
        """ Test Page Links

        Scrape the page for links and ensure none return HTTP/404.

        Test failure denotes a link on a page that should not exist within the template.

        Args:
            url (str): Page to test
        """

        response = self.session.get(
            url = str(self.server_url + url)
        )

        # Failsafe to ensure no redirection and that page exists
        assert len(response.history) == 0
        assert response.status_code == 200

        page_urls = []

        page = str(response.content)

        links = re.findall('href=\"([a-z\/0-9]+)\"', page)

        for link in links:

            page_link_response = self.session.get(
                url = str(self.server_url + link)
            )

            # Failsafe to ensure no redirection
            assert len(response.history) == 0

            assert page_link_response.status_code != 404

