import pytest
import unittest
import requests

from django.contrib.auth.models import User, Permission
from django.shortcuts import reverse
from django.test import Client, TestCase



class PermissionPermissionsAPI(TestCase):

    model = Permission

    app_namespace = 'API'
    
    url_name = '_api_v2_permission'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. create a user
        """

        self.url_kwargs = {}

        self.url_view_kwargs = {'pk': 1}

        self.view_user = User.objects.create_user(username="test_user_view", password="password")



    def test_view_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 401


    def test_view_authenticated_user(self):
        """ Check correct permission for view

        Attempt to view as user who is authenticated
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200
