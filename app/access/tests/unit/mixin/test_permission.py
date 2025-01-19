import pytest
from unittest.mock import Mock, patch

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rest_framework.generics import GenericAPIView

from access.middleware.request import Tenancy

from api.viewsets.common import ModelViewSet

from access.mixins.organization import OrganizationMixin
from access.mixins.permissions import OrganizationPermissionMixin
from access.models import Organization, Team, TeamUsers, Permission

from core import exceptions as centurion_exceptions
from core.models.manufacturer import Manufacturer

from settings.models.app_settings import AppSettings



class MyMockView(
    ModelViewSet
):

    class MockRequest:

        class MockStream:

            method: str = None

            def __init__(self, method: str):

                self.method = method

        data: dict = None

        method: str = None

        # query_params: dict = {}

        stream: MockStream = None

        _stream: MockStream = None



        tenancy: Tenancy = None



        def __init__(self, data: dict, method: str, user: User, tenancy: Tenancy):

            self.data = data

            self.method = method

            # self._stream = self.MockStream( method = method )

            # self.stream = self._stream

            self.user = user

            self.tenancy = tenancy


    action: str = None
    """create, destroy, list, metadata, retrieve, partial_updata, update"""

    allowed_methods: list = []

    kwargs: dict = None

    model = None

    mocked_object = None

    request: MockRequest = None

    def __init__(self, action:str, kwargs: dict, method: str, model, obj, user: User, data:dict = None):

        self.action = action

        self.allowed_methods += [ method ]

        self.kwargs = kwargs

        self.model = model

        self.mocked_object = obj

        tenancy = Tenancy(
                user = user,
                app_settings = AppSettings.objects.get(
                    owner_organization = None
                )
            )

        self.request = self.MockRequest(
            data = data,
            method = method,
            user = user,
            tenancy = tenancy
        )




class OrganizationPermissionSetup:


    model = Manufacturer


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. 
        """

        self.organization = Organization.objects.create(name='test_org1', model_notes='random text')

        self.organization_two = Organization.objects.create(name='test_org2', model_notes='random text')

        self.organization_three = Organization.objects.create(name='test_org3', model_notes='random text')



        add_permissions = Permission.objects.get(
            codename = 'add_' + self.model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = self.model._meta.app_label,
                model = self.model._meta.model_name,
            )
        )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = self.organization,
        )

        add_team.permissions.set([add_permissions])

        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )


        add_team_two = Team.objects.create(
            team_name = 'add_team',
            organization = self.organization_two,
        )

        add_team_two.permissions.set([add_permissions])

        self.add_user_two = User.objects.create_user(username="test_user_add_two", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team_two,
            user = self.add_user_two
        )









        change_permissions = Permission.objects.get(
            codename = 'change_' + self.model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = self.model._meta.app_label,
                model = self.model._meta.model_name,
            )
        )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = self.organization,
        )

        change_team.permissions.set([change_permissions])

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )



        change_team_two = Team.objects.create(
            team_name = 'change_team_two',
            organization = self.organization_two,
        )

        change_team_two.permissions.set([change_permissions])

        self.change_user_two = User.objects.create_user(username="test_user_change_two", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team_two,
            user = self.change_user_two
        )





        delete_permissions = Permission.objects.get(
            codename = 'delete_' + self.model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = self.model._meta.app_label,
                model = self.model._meta.model_name,
            )
        )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = self.organization,
        )

        delete_team.permissions.set([delete_permissions])

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        delete_team_two = Team.objects.create(
            team_name = 'delete_team',
            organization = self.organization_two,
        )

        delete_team_two.permissions.set([delete_permissions])

        self.delete_user_two = User.objects.create_user(username="test_user_delete_two", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team_two,
            user = self.delete_user_two
        )




        view_permissions = Permission.objects.get(
            codename = 'view_' + self.model._meta.model_name,
            content_type = ContentType.objects.get(
                app_label = self.model._meta.app_label,
                model = self.model._meta.model_name,
            )
        )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        view_team_two = Team.objects.create(
            team_name = 'view_team_two',
            organization = self.organization_two,
        )

        view_team_two.permissions.set([view_permissions])


        self.view_user_two = User.objects.create_user(username="test_user_view_two", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team_two,
            user = self.view_user_two
        )








        self.obj = self.model.objects.create(
            organization = self.organization,
            name = 'man 1',
        )



class HasPermissionCommon(
    OrganizationPermissionSetup,
):



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission(self, get_object):

        get_object.return_value = self.obj


        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj


        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view)



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj


        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj


        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False


class HasPermission(
    HasPermissionCommon,
):


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_function_get_object_called_once(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj


        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.call_count == 1




class HasPermissionWrongMethodOptions:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class HasPermissionWrongMethodDelete:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class HasPermissionWrongMethodGet:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class HasPermissionWrongMethodPatch:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class HasPermissionWrongMethodPost:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False





    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





class HasPermissionWrongMethodPut:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False




    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class HasPermissionDifferentOrganizationCommon:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False





    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



class HasPermissionDifferentOrganization(
    HasPermissionDifferentOrganizationCommon,
):

    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_get_object_called_once(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.call_count == 1





class HasPermissionDifferentOrganizationWrongMethodDelete:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)






class HasPermissionDifferentOrganizationWrongMethodGet:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_Get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_Get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_Get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class HasPermissionDifferentOrganizationWrongMethodOptions:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class HasPermissionDifferentOrganizationWrongMethodPatch:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class HasPermissionDifferentOrganizationWrongMethodPost:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class HasPermissionDifferentOrganizationWrongMethodPut:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)







class ActionDeniedAddPermission:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False





    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



class ActionDeniedAddPermissionWrongMethodDelete:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False




    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedAddPermissionWrongMethodGet:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedAddPermissionWrongMethodOptions:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedAddPermissionWrongMethodPatch:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedAddPermissionWrongMethodPost:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedAddPermissionWrongMethodPut:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_add_permission_denied_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.add_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedChangePermission:




    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False






    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False






class ActionDeniedChangePermissionWrongMethodDelete:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False




    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)






class ActionDeniedChangePermissionWrongMethodGet:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedChangePermissionWrongMethodOptions:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedChangePermissionWrongMethodPatch:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedChangePermissionWrongMethodPost:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedChangePermissionWrongMethodPut:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_change_permission_denied_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.change_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)








class ActionDeniedDeletePermission:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False





    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



class ActionDeniedDeletePermissionWrongMethodDelete:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





class ActionDeniedDeletePermissionWrongMethodGet:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedDeletePermissionWrongMethodOptions:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





class ActionDeniedDeletePermissionWrongMethodPatch:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedDeletePermissionWrongMethodPost:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedDeletePermissionWrongMethodPut:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_delete_permission_denied_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.delete_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)








class ActionDeniedViewPermission:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False





    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False


    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



class ActionDeniedViewPermissionWrongMethodOptions:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_options_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedViewPermissionWrongMethodDelete:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False




    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_delete_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedViewPermissionWrongMethodGet:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_get_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedViewPermissionWrongMethodPatch:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_patch_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedViewPermissionWrongMethodPost:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_post_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





class ActionDeniedViewPermissionWrongMethodPut:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        assert OrganizationPermissionMixin().has_permission(request = view.request, view = view) is False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert get_object.called == False



    @patch.object(GenericAPIView, 'get_object')
    def test_action_view_permission_denied_wrong_method_put_raised_method_not_allowed(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = self.view_user,
        )

        view.allowed_methods = [
            self.http_method
        ]

        with pytest.raises( centurion_exceptions.MethodNotAllowed ) as ex:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)






class ActionDeniedAnonymousUser:



    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_head(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_head_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'HEAD',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)



class ActionDeniedAnonymousUserWrongMethodDelete:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_delete(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_delete_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'DELETE',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedAnonymousUserWrongMethodGet:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_get(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_get_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'GET',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedAnonymousUserWrongMethodOptions:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_options(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_options_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'OPTIONS',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




class ActionDeniedAnonymousUserWrongMethodPatch:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_patch(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_patch_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PATCH',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


class ActionDeniedAnonymousUserWrongMethodPost:


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_post(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)


    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_post_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'POST',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)





class ActionDeniedAnonymousUserWrongMethodPut:

    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_put(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




    @patch.object(GenericAPIView, 'get_object')
    def test_action_anon_user_denied_wrong_method_put_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = 'PUT',
            model = self.model,
            obj = obj,
            user = AnonymousUser(),
        )

        with pytest.raises(centurion_exceptions.NotAuthenticated) as err:

            OrganizationPermissionMixin().has_permission(request = view.request, view = view)




































































class AddOrganizationPermissions(
    # ActionDeniedAddPermission,
    # ActionDeniedAddPermissionWrongMethodDelete,
    # ActionDeniedAddPermissionWrongMethodGet,
    # ActionDeniedAddPermissionWrongMethodOptions,
    # ActionDeniedAddPermissionWrongMethodPatch,
    # ActionDeniedAddPermissionWrongMethodPost,
    # ActionDeniedAddPermissionWrongMethodPut,
    ActionDeniedAnonymousUser,
    ActionDeniedAnonymousUserWrongMethodDelete,
    ActionDeniedAnonymousUserWrongMethodGet,
    ActionDeniedAnonymousUserWrongMethodOptions,
    ActionDeniedAnonymousUserWrongMethodPatch,
    ActionDeniedAnonymousUserWrongMethodPost,
    ActionDeniedAnonymousUserWrongMethodPut,
    ActionDeniedChangePermission,
    ActionDeniedChangePermissionWrongMethodDelete,
    ActionDeniedChangePermissionWrongMethodGet,
    ActionDeniedChangePermissionWrongMethodOptions,
    ActionDeniedChangePermissionWrongMethodPatch,
    # ActionDeniedChangePermissionWrongMethodPost,
    ActionDeniedChangePermissionWrongMethodPut,
    ActionDeniedDeletePermission,
    ActionDeniedDeletePermissionWrongMethodDelete,
    ActionDeniedDeletePermissionWrongMethodGet,
    ActionDeniedDeletePermissionWrongMethodOptions,
    ActionDeniedDeletePermissionWrongMethodPatch,
    # ActionDeniedDeletePermissionWrongMethodPost,
    ActionDeniedDeletePermissionWrongMethodPut,
    ActionDeniedViewPermission,
    ActionDeniedViewPermissionWrongMethodDelete,
    ActionDeniedViewPermissionWrongMethodGet,
    ActionDeniedViewPermissionWrongMethodOptions,
    ActionDeniedViewPermissionWrongMethodPatch,
    # ActionDeniedViewPermissionWrongMethodPost,
    ActionDeniedViewPermissionWrongMethodPut,
    HasPermissionCommon,
    HasPermissionWrongMethodDelete,
    HasPermissionWrongMethodGet,
    HasPermissionWrongMethodOptions,
    HasPermissionWrongMethodPatch,
    # HasPermissionWrongMethodPost,
    HasPermissionWrongMethodPut,
    HasPermissionDifferentOrganizationCommon,
    HasPermissionDifferentOrganizationWrongMethodDelete,
    HasPermissionDifferentOrganizationWrongMethodGet,
    HasPermissionDifferentOrganizationWrongMethodOptions,
    HasPermissionDifferentOrganizationWrongMethodPatch,
    # HasPermissionDifferentOrganizationWrongMethodPost,
    HasPermissionDifferentOrganizationWrongMethodPut,
    TestCase,
):

    http_method = 'POST'

    view_action = 'create'



    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.test_user = self.add_user

        self.test_user_two = self.add_user_two


        self.add_data: dict = {
            'organization': self.organization.id,
            'name': 'item_added_post'
        }



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_different_org_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj

        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user_two,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert not get_object.called



    @patch.object(GenericAPIView, 'get_object')
    def test_action_has_permission_function_get_object_not_called(self, get_object):

        get_object.return_value = self.obj

        if hasattr(self, 'add_data'):

            data = self.add_data

            kwargs = {}

            obj = None

        else:

            data = None

            kwargs = {
                'pk': self.obj.id
            }

            obj = self.obj


        view = MyMockView(
            action = self.view_action,
            data = data,
            kwargs = kwargs,
            method = self.http_method,
            model = self.model,
            obj = obj,
            user = self.test_user,
        )

        OrganizationPermissionMixin().has_permission(request = view.request, view = view)

        assert not get_object.called






class ChangeOrganizationPermissions(
    ActionDeniedAddPermission,
    ActionDeniedAddPermissionWrongMethodDelete,
    ActionDeniedAddPermissionWrongMethodGet,
    ActionDeniedAddPermissionWrongMethodOptions,
    ActionDeniedAddPermissionWrongMethodPatch,
    ActionDeniedAddPermissionWrongMethodPost,
    # ActionDeniedAddPermissionWrongMethodPut,
    ActionDeniedAnonymousUser,
    ActionDeniedAnonymousUserWrongMethodDelete,
    ActionDeniedAnonymousUserWrongMethodGet,
    ActionDeniedAnonymousUserWrongMethodOptions,
    ActionDeniedAnonymousUserWrongMethodPatch,
    ActionDeniedAnonymousUserWrongMethodPost,
    ActionDeniedAnonymousUserWrongMethodPut,
    # ActionDeniedChangePermission,
    # ActionDeniedChangePermissionWrongMethodGet,
    # ActionDeniedChangePermissionWrongMethodOptions,
    # ActionDeniedChangePermissionWrongMethodPatch,
    # ActionDeniedChangePermissionWrongMethodPost,
    # ActionDeniedChangePermissionWrongMethodPut,
    ActionDeniedDeletePermission,
    ActionDeniedDeletePermissionWrongMethodDelete,
    ActionDeniedDeletePermissionWrongMethodGet,
    ActionDeniedDeletePermissionWrongMethodOptions,
    ActionDeniedDeletePermissionWrongMethodPatch,
    ActionDeniedDeletePermissionWrongMethodPost,
    # ActionDeniedDeletePermissionWrongMethodPut,
    ActionDeniedViewPermission,
    ActionDeniedViewPermissionWrongMethodDelete,
    ActionDeniedViewPermissionWrongMethodGet,
    ActionDeniedViewPermissionWrongMethodOptions,
    ActionDeniedViewPermissionWrongMethodPatch,
    ActionDeniedViewPermissionWrongMethodPost,
    # ActionDeniedViewPermissionWrongMethodPut,
    HasPermission,
    HasPermissionWrongMethodDelete,
    HasPermissionWrongMethodGet,
    HasPermissionWrongMethodOptions,
    HasPermissionWrongMethodPatch,
    HasPermissionWrongMethodPost,
    # HasPermissionWrongMethodPut,
    HasPermissionDifferentOrganization,
    HasPermissionDifferentOrganizationWrongMethodDelete,
    HasPermissionDifferentOrganizationWrongMethodGet,
    HasPermissionDifferentOrganizationWrongMethodOptions,
    HasPermissionDifferentOrganizationWrongMethodPatch,
    HasPermissionDifferentOrganizationWrongMethodPost,
    # HasPermissionDifferentOrganizationWrongMethodPut,
    TestCase,
):

    http_method = 'PUT'

    view_action = 'update'



    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.test_user = self.change_user

        self.test_user_two = self.change_user_two




class DeleteOrganizationPermissions(
    ActionDeniedAddPermission,
    # ActionDeniedAddPermissionWrongMethodDelete,
    ActionDeniedAddPermissionWrongMethodGet,
    ActionDeniedAddPermissionWrongMethodOptions,
    ActionDeniedAddPermissionWrongMethodPatch,
    ActionDeniedAddPermissionWrongMethodPost,
    ActionDeniedAddPermissionWrongMethodPut,
    ActionDeniedAnonymousUser,
    ActionDeniedAnonymousUserWrongMethodDelete,
    ActionDeniedAnonymousUserWrongMethodGet,
    ActionDeniedAnonymousUserWrongMethodOptions,
    ActionDeniedAnonymousUserWrongMethodPatch,
    ActionDeniedAnonymousUserWrongMethodPost,
    ActionDeniedAnonymousUserWrongMethodPut,
    ActionDeniedChangePermission,
    # ActionDeniedChangePermissionWrongMethodDelete,
    ActionDeniedChangePermissionWrongMethodGet,
    ActionDeniedChangePermissionWrongMethodOptions,
    ActionDeniedChangePermissionWrongMethodPatch,
    ActionDeniedChangePermissionWrongMethodPost,
    ActionDeniedChangePermissionWrongMethodPut,
    # ActionDeniedDeletePermission,
    # ActionDeniedDeletePermissionWrongMethodDelete,
    # ActionDeniedDeletePermissionWrongMethodGet,
    # ActionDeniedDeletePermissionWrongMethodOptions,
    # ActionDeniedDeletePermissionWrongMethodPatch,
    # ActionDeniedDeletePermissionWrongMethodPost,
    # ActionDeniedDeletePermissionWrongMethodPut,
    ActionDeniedViewPermission,
    # ActionDeniedViewPermissionWrongMethodDelete,
    ActionDeniedViewPermissionWrongMethodGet,
    ActionDeniedViewPermissionWrongMethodOptions,
    ActionDeniedViewPermissionWrongMethodPatch,
    ActionDeniedViewPermissionWrongMethodPost,
    ActionDeniedViewPermissionWrongMethodPut,
    HasPermission,
    # HasPermissionWrongMethodDelete,
    HasPermissionWrongMethodGet,
    HasPermissionWrongMethodOptions,
    HasPermissionWrongMethodPatch,
    HasPermissionWrongMethodPost,
    HasPermissionWrongMethodPut,
    HasPermissionDifferentOrganization,
    # HasPermissionDifferentOrganizationWrongMethodDelete,
    HasPermissionDifferentOrganizationWrongMethodGet,
    HasPermissionDifferentOrganizationWrongMethodOptions,
    HasPermissionDifferentOrganizationWrongMethodPatch,
    HasPermissionDifferentOrganizationWrongMethodPost,
    HasPermissionDifferentOrganizationWrongMethodPut,
    TestCase,
):

    http_method = 'DELETE'

    view_action = 'destroy'



    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.test_user = self.delete_user

        self.test_user_two = self.delete_user_two






class PartialChangeOrganizationPermissions(
    ActionDeniedAddPermission,
    ActionDeniedAddPermissionWrongMethodDelete,
    ActionDeniedAddPermissionWrongMethodGet,
    ActionDeniedAddPermissionWrongMethodOptions,
    # ActionDeniedAddPermissionWrongMethodPatch,
    ActionDeniedAddPermissionWrongMethodPost,
    ActionDeniedAddPermissionWrongMethodPut,
    ActionDeniedAnonymousUser,
    ActionDeniedAnonymousUserWrongMethodDelete,
    ActionDeniedAnonymousUserWrongMethodGet,
    ActionDeniedAnonymousUserWrongMethodOptions,
    ActionDeniedAnonymousUserWrongMethodPatch,
    ActionDeniedAnonymousUserWrongMethodPost,
    ActionDeniedAnonymousUserWrongMethodPut,
    # ActionDeniedChangePermission,
    # ActionDeniedChangePermissionWrongMethodGet,
    # ActionDeniedChangePermissionWrongMethodOptions,
    # ActionDeniedChangePermissionWrongMethodPatch,
    # ActionDeniedChangePermissionWrongMethodPost,
    # ActionDeniedChangePermissionWrongMethodPut,
    ActionDeniedDeletePermission,
    ActionDeniedDeletePermissionWrongMethodDelete,
    ActionDeniedDeletePermissionWrongMethodGet,
    ActionDeniedDeletePermissionWrongMethodOptions,
    # ActionDeniedDeletePermissionWrongMethodPatch,
    ActionDeniedDeletePermissionWrongMethodPost,
    ActionDeniedDeletePermissionWrongMethodPut,
    ActionDeniedViewPermission,
    ActionDeniedViewPermissionWrongMethodDelete,
    ActionDeniedViewPermissionWrongMethodGet,
    ActionDeniedViewPermissionWrongMethodOptions,
    # ActionDeniedViewPermissionWrongMethodPatch,
    ActionDeniedViewPermissionWrongMethodPost,
    ActionDeniedViewPermissionWrongMethodPut,
    HasPermission,
    HasPermissionWrongMethodDelete,
    HasPermissionWrongMethodGet,
    HasPermissionWrongMethodOptions,
    # HasPermissionWrongMethodPatch,
    HasPermissionWrongMethodPost,
    HasPermissionWrongMethodPut,
    HasPermissionDifferentOrganization,
    HasPermissionDifferentOrganizationWrongMethodDelete,
    HasPermissionDifferentOrganizationWrongMethodGet,
    HasPermissionDifferentOrganizationWrongMethodOptions,
    # HasPermissionDifferentOrganizationWrongMethodPatch,
    HasPermissionDifferentOrganizationWrongMethodPost,
    HasPermissionDifferentOrganizationWrongMethodPut,
    TestCase,
):

    http_method = 'PATCH'

    view_action = 'partial_update'



    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.test_user = self.change_user

        self.test_user_two = self.change_user_two





class ViewOrganizationPermissions(
    ActionDeniedAddPermission,
    ActionDeniedAddPermissionWrongMethodDelete,
    # ActionDeniedAddPermissionWrongMethodGet,
    ActionDeniedAddPermissionWrongMethodOptions,
    ActionDeniedAddPermissionWrongMethodPatch,
    ActionDeniedAddPermissionWrongMethodPost,
    ActionDeniedAddPermissionWrongMethodPut,
    ActionDeniedAnonymousUser,
    ActionDeniedAnonymousUserWrongMethodDelete,
    ActionDeniedAnonymousUserWrongMethodGet,
    ActionDeniedAnonymousUserWrongMethodOptions,
    ActionDeniedAnonymousUserWrongMethodPatch,
    ActionDeniedAnonymousUserWrongMethodPost,
    ActionDeniedAnonymousUserWrongMethodPut,
    ActionDeniedChangePermission,
    ActionDeniedChangePermissionWrongMethodDelete,
    # ActionDeniedChangePermissionWrongMethodGet,
    ActionDeniedChangePermissionWrongMethodOptions,
    ActionDeniedChangePermissionWrongMethodPatch,
    ActionDeniedChangePermissionWrongMethodPost,
    ActionDeniedChangePermissionWrongMethodPut,
    ActionDeniedDeletePermission,
    ActionDeniedDeletePermissionWrongMethodDelete,
    # ActionDeniedDeletePermissionWrongMethodGet,
    ActionDeniedDeletePermissionWrongMethodOptions,
    ActionDeniedDeletePermissionWrongMethodPatch,
    ActionDeniedDeletePermissionWrongMethodPost,
    ActionDeniedDeletePermissionWrongMethodPut,
    # ActionDeniedViewPermission,
    # ActionDeniedViewPermissionWrongMethodDelete,
    # ActionDeniedViewPermissionWrongMethodGet,
    # ActionDeniedViewPermissionWrongMethodOptions,
    # ActionDeniedViewPermissionWrongMethodPatch,
    # ActionDeniedViewPermissionWrongMethodPost,
    # ActionDeniedViewPermissionWrongMethodPut,
    HasPermission,
    HasPermissionWrongMethodDelete,
    # HasPermissionWrongMethodGet,
    HasPermissionWrongMethodOptions,
    HasPermissionWrongMethodPatch,
    HasPermissionWrongMethodPost,
    HasPermissionWrongMethodPut,
    HasPermissionDifferentOrganization,
    HasPermissionDifferentOrganizationWrongMethodDelete,
    # HasPermissionDifferentOrganizationWrongMethodGet,
    HasPermissionDifferentOrganizationWrongMethodOptions,
    HasPermissionDifferentOrganizationWrongMethodPatch,
    HasPermissionDifferentOrganizationWrongMethodPost,
    HasPermissionDifferentOrganizationWrongMethodPut,
    TestCase,
):

    http_method = 'GET'

    view_action = 'retrieve'



    @classmethod
    def setUpTestData(self):

        super().setUpTestData()


        self.test_user = self.view_user

        self.test_user_two = self.view_user_two