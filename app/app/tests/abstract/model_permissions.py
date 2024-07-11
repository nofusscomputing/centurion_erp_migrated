import pytest
import unittest

from django.test import Client
from django.shortcuts import reverse



class ModelPermissionsView:
    """ Tests for checking model view permissions """


    app_namespace: str = None

    url_name_view: str

    url_view_kwargs: dict = None



    def test_model_view_user_anon_denied(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()

        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_model_view_no_permission_denied(self):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_model_view_different_organizaiton_denied(self):
        """ Check correct permission for view

        Attempt to view with user from different organization
        """

        client = Client()
        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)


        client.force_login(self.different_organization_user)
        response = client.get(url)

        assert response.status_code == 403


    def test_model_view_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        if self.app_namespace:

            url = reverse(self.app_namespace + ':' + self.url_name_view, kwargs=self.url_view_kwargs)

        else:

            url = reverse(self.url_name_view, kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200



class ModelPermissionsAdd:
    """ Tests for checking model Add permissions """

    app_namespace: str = None

    url_name_add: str

    url_add_kwargs: dict = None

    add_data: dict = None


    @pytest.mark.skip(reason="ToDO: write test")
    def test_model_requires_attribute_parent_model(self):
        """ Child model requires 'django view' attribute 'parent_model'
        
        When a child-model is added the parent model is required so that the organization can be detrmined.
        """

        pass


    def test_model_add_user_anon_denied(self):
        """ Check correct permission for add 

        Attempt to add as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        response = client.put(url, data=self.add_data)

        assert response.status_code == 302 and response.url.startswith('/account/login')

    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_model_add_no_permission_denied(self):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    # @pytest.mark.skip(reason="ToDO: figure out why fails")
    def test_model_add_different_organization_denied(self):
        """ Check correct permission for add

        attempt to add as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    def test_model_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.view_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403


    def test_model_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with no permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 200



class ModelPermissionsChange:
    """ Tests for checking model change permissions """

    app_namespace: str = None

    url_name_change: str

    url_change_kwargs: dict = None

    change_data: dict = None


    def test_model_change_user_anon_denied(self):
        """ Check correct permission for change

        Attempt to change as anon
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        response = client.patch(url, data=self.change_data)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_model_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 403


    def test_model_change_different_organization_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        client.force_login(self.different_organization_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 403


    def test_model_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        client.force_login(self.view_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 403


    def test_model_change_permission_add_denied(self):
        """ Ensure permission view cant make change

        Attempt to make change as user with add permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        client.force_login(self.add_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 403


    def test_model_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)


        client.force_login(self.change_user)
        response = client.post(url, data=self.change_data)

        assert response.status_code == 200



class ModelPermissionsDelete:
    """ Tests for checking model delete permissions """

    app_namespace: str = None

    url_name_delete: str

    url_delete_kwargs: dict = None

    url_delete_response: str

    delete_data: dict = None

    def test_model_delete_user_anon_denied(self):
        """ Check correct permission for delete

        Attempt to delete item as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 302 and response.url.startswith('/account/login')


    def test_model_delete_no_permission_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.no_permissions_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_model_delete_different_organization_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user from different organization
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.different_organization_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_model_delete_permission_view_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with veiw permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.view_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_model_delete_permission_add_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with add permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.add_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_model_delete_permission_change_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with change permission only
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.change_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403


    def test_model_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name_delete, kwargs=self.url_delete_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 302 and response.url == self.url_delete_response


class ModelPermissions(
    ModelPermissionsView,
    ModelPermissionsAdd,
    ModelPermissionsChange,
    ModelPermissionsDelete
):
    """ Tests for checking model permissions """

    app_namespace: str = None
