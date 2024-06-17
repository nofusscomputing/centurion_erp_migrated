import pytest
import unittest

from django.test import Client
from django.shortcuts import reverse



class OrganizationManagerModelPermissionView:
    """ Tests for checking Organization Manager model permissions """


    app_namespace: str = None
    """ Application namespace of the model being tested """

    different_organization_is_manager: object
    """ User whom is organization Manager of different organization than object """

    url_name_view: str
    """ url name of the model view to be tested """

    url_view_kwargs: dict = None
    """ View URL kwargs for model being tested """

    user_is_organization_manager: object
    """ User whom is organization Manager of the object"""



    def test_model_view_different_organizaiton_is_organization_manager_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization whom is an organization Manager.
        """

        client = Client()
        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_is_manager)
        response = client.get(url)

        assert response.status_code == 403


    def test_model_view_has_no_permission_is_organization_manager(self):
        """ Confirm that an organization manager can view the model 

        Attempt to view as user who is an organization manager and has no permissions assigned.
        Object to be within same organization the user is a manager of.
        """

        client = Client()
        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)


        client.force_login(self.user_is_organization_manager)
        response = client.get(url)

        assert response.status_code == 200


class OrganizationManagerModelPermissions(
    OrganizationManagerModelPermissionView,
):
    """ Tests for checking Organization Manager model permissions
    
    This class includes all test cases for: Add, Change, Delete and View.
    """

    app_namespace: str = None
