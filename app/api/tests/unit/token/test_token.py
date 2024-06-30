import hashlib
import json
import pytest
import requests
import unittest

from datetime import datetime, timedelta

from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import reverse
from django.test import TestCase, Client

from access.models import Organization, Team, TeamUsers, Permission

from api.models.tokens import AuthToken

from settings.models.user_settings import UserSettings

class APIAuthToken(TestCase):



    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        3. create user
        4. create user settings
        5. create API key (valid)
        6. generate an API key that does not exist
        5. create API key (expired)
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        add_user_settings = UserSettings.objects.get(user=self.add_user)

        add_user_settings.default_organization = organization

        add_user_settings.save()

        expires = datetime.utcnow() + timedelta(days = 10)

        expires = expires.strftime('%Y-%m-%d %H:%M:%S%z')

        token = AuthToken.objects.create(
            user = self.add_user,
            expires=expires
        )

        self.api_token_valid = token.generate()
        self.hashed_token = token.token_hash(self.api_token_valid)
        token.token = self.hashed_token

        token.save()

        self.api_token_does_not_exist = hashlib.sha256(str('a random string').encode('utf-8')).hexdigest()


        expires = datetime.utcnow() + timedelta(days = -10)

        expires = expires.strftime('%Y-%m-%d %H:%M:%S%z')


        self.api_token_expired = token.generate()

        self.hashed_token_expired = token.token_hash(self.api_token_expired)

        token = AuthToken.objects.create(
            user = self.add_user,
            expires=expires,
            token = self.hashed_token_expired
        )



    def test_token_create_own(self):
        """ Check correct permission for add 

        User can only create token for self.
        """

        client = Client()
        client.force_login(self.add_user)
        url = reverse('_user_auth_token_add', kwargs={'user_id': self.add_user.id})


        response = client.post(url, kwargs={'user_id': self.add_user.id})

        assert response.status_code == 200



    def test_token_create_other_user(self):
        """ Check correct permission for add 

        User can not create token for another user.
        """

        client = Client()
        client.force_login(self.add_user)
        url = reverse('_user_auth_token_add', kwargs={'user_id': 999})


        response = client.post(url, kwargs={'user_id': 999})

        assert response.status_code == 403



    def test_token_delete_own(self):
        """ Check correct permission for delete 

        User can only delete token for self.
        """

        client = Client()
        client.force_login(self.add_user)
        url = reverse('_user_auth_token_delete', kwargs={'user_id': self.add_user.id, 'pk': 1})


        response = client.post(url, kwargs={'user_id': self.add_user.id, 'pk': 1})

        assert response.status_code == 302 and response.url == '/account/settings/1'



    def test_token_delete_other_user(self):
        """ Check correct permission for delete 

        User can not delete another users token.
        """

        client = Client()
        client.force_login(self.add_user)
        url = reverse('_user_auth_token_delete', kwargs={'user_id': 999, 'pk': 1})


        response = client.post(url, data={'id': 1}, kwargs={'user_id': 999, 'pk': 1})

        assert response.status_code == 403



    def test_auth_invalid_token(self):
        """ Check token authentication

        Invalid token does not allow login
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token ' + self.api_token_does_not_exist,
            }
        )

        assert response.status_code == 401



    def test_auth_no_token(self):
        """ Check token authentication

        providing no token does not allow login
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json'
            }
        )

        assert response.status_code == 401



    def test_auth_expired_token(self):
        """ Check token authentication

        expired token does not allow login
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token ' + self.api_token_expired,
            }
        )

        assert response.status_code == 401



    def test_auth_valid_token(self):
        """ Check token authentication

        Valid token allows login
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token ' + self.api_token_valid,
            }
        )

        assert response.status_code == 200



    def test_feat_expired_token_is_removed(self):
        """ token feature confirmation

        expired token is deleted
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token ' + self.api_token_expired,
            }
        )

        db_query = AuthToken.objects.filter(
            token = self.hashed_token_expired
        )
        
        assert not db_query.exists()



    def test_token_not_saved_to_db(self):
        """ confirm generated token not saved to the database """

        db_query = AuthToken.objects.filter(
            token = self.api_token_valid
        )

        assert not db_query.exists()



    def test_header_format_invalid_token(self):
        """ token header format check
        
        header missing 'Token' prefix reports invalid
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': '' + self.api_token_valid,
            }
        )

        content: dict = json.loads(response.content.decode('utf-8'))

        assert response.status_code == 401 and content['detail'] == 'Token header invalid'



    def test_header_format_invalid_token_spaces(self):
        """ token header format check
        
        auth header with extra spaces reports invalid
        """

        client = Client()
        url = reverse('home') + 'api/'


        response = client.get(
            url,
            content_type='application/json',
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Token A space ' + self.api_token_valid,
            }
        )

        content: dict = json.loads(response.content.decode('utf-8'))

        assert response.status_code == 401 and content['detail'] == 'Token header invalid. Possibly incorrectly formatted'

