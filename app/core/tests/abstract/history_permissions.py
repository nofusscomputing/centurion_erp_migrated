import pytest
import unittest

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, Client

from core.models.history import History

from itam.models.device import Device



class HistoryPermissions:
    """Test cases for accessing History """    


    item: object
    """Created Model

    Create a new item. 
    """

    model = History
    """ The history Model """

    namespace: str = ''
    """ URL namespace for the history view"""

    name_view: str = '_history'
    """ URL view name for history """

    no_permissions_user: User
    """A User with no permissions to access the item
    
    Create in `setUpTestData`
    """

    different_organization_user: User
    """A User with the correct permissions to access the item

    This user must be in a different organization than the item
    
    Create in `setUpTestData`
    """

    view_user: User
    """A User with the correct permissions to access the item

    This user must be in the same organization as the item
    
    Create in `setUpTestData`
    """


    def test_view_history_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.namespace + self.name_view, kwargs={'model_name': self.item._meta.model_name, 'model_pk': self.item.id})

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_view_history_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.item._meta.model_name, 'model_pk': self.item.id})


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_view_history_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.item._meta.model_name, 'model_pk': self.item.id})


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_view_history_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.namespace +  self.name_view, kwargs={'model_name': self.item._meta.model_name, 'model_pk': self.item.id})


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200
