import pytest
import unittest

from django.shortcuts import reverse
from django.test import TestCase, Client



class APIPermissionView:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """


    def test_view_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 401


    def test_view_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_view_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200



class APIPermissionAdd:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_list: str
    """ URL view name of the item list page """

    url_kwargs: dict = None
    """ URL view kwargs for the item list page """

    add_data: dict = None


    def test_add_user_anon_denied(self):
        """ Check correct permission for add 

        Attempt to add as anon user
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_list, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_list)


        response = client.put(url, data=self.add_data)

        assert response.status_code == 401

    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_add_no_permission_denied(self):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_list, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_add_different_organization_denied(self):
        """ Check correct permission for add

        attempt to add as user from different organization
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_list, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    def test_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_list, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.view_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    def test_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with no permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_list, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 201



class APIPermissionChange:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    change_data: dict = None


    def test_change_user_anon_denied(self):
        """ Check correct permission for change

        Attempt to change as anon
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 401


    def test_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403


    def test_change_different_organization_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403


    def test_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403


    def test_change_permission_add_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.add_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 403


    def test_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 200



class APIPermissionDelete:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    delete_data: dict = None


    def test_delete_user_anon_denied(self):
        """ Check correct permission for delete

        Attempt to delete item as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 401


    def test_delete_no_permission_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_delete_different_organization_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_delete_permission_view_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with veiw permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_delete_permission_add_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with add permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.add_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_delete_permission_change_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with change permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name, kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 204



class APIPermissions(
    APIPermissionAdd,
    APIPermissionChange,
    APIPermissionDelete,
    APIPermissionView
):
    """ Abstract class containing all API Permission test cases """

    model: object
    """ Item Model to test """
