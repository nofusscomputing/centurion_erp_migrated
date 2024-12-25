import traceback

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import exceptions
from rest_framework.permissions import DjangoObjectPermissions

from access.models import TenancyObject

from core import exceptions as centurion_exceptions



class OrganizationPermissionMixin(
    DjangoObjectPermissions,
):
    """Organization Permission Mixin

    This class is to be used as the permission class for API `Views`/`ViewSets`.
    In combination with the `OrganizationPermissionsMixin`, permission checking
    will be done to ensure the user has the correct permissions to perform the
    CRUD operation.

    **Note:** If the user is not authenticated, they will be denied access
    globally.

    Permissions are broken down into two areas:
    
    - `Tenancy` Objects

        This object requires that the user have the correct permission and that
        permission be assigned within the organiztion the object belongs to.

    - `Non-Tenancy` Objects.

        This object requires the the use have the correct permission assigned,
        regardless of the organization the object is from. This includes objects
        that have no organization.

    """

    def has_permission(self, request, view):
        """ Check if user has the required permission

        Args:
            request (object): The HTTP Request Object
            view (_type_): The View/Viewset Object the request was made to

        Raises:
            ValueError: Could not determin the view action.

        Returns:
            True (bool): User has the required permission.
            False (bool): User does not have the required permission
        """

        if request.user.is_anonymous:

            return False

        try:


            view.get_user_organizations( request.user )

            obj_organization: Organization = view.get_obj_organization(
                request = request
            )


            if(
                view.action == 'create'
                or getattr(view.request._stream, 'method', '') == 'POST'
            ):

                view_action = 'add'

            elif (
                view.action == 'partial_update'
                or view.action == 'update'
                or getattr(view.request._stream, 'method', '') == 'PATCH'
                or getattr(view.request._stream, 'method', '') == 'PUT'
            ):

                view_action = 'change'

                obj_organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif view.action == 'destroy':

                view_action = 'delete'

                obj_organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif (
                view.action == 'list'
            ):

                view_action = 'view'

            elif view.action == 'retrieve':

                view_action = 'view'

                obj_organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif view.action == 'metadata':

                return True

            
            if view_action is None:

                raise ValueError('view_action could not be defined.')


            has_permission_required: bool = False

            if getattr(view, '_user_permissions', []):

                has_permission_required = view.get_permission_required() in getattr(view, '_user_permissions', [])


                return True

            elif(
                obj_organization is not None
                and is_tenancy_model
            ):


                if view.has_organization_permission(
                    organization = obj_organization.id,
                    permissions_required = [ self.permission_required ]
                ):

                    return True

            elif(
                self.permission_required in getattr(view, '_user_permissions', [])
                and view.action == 'list'
            ):

                return True


        except ValueError:

            pass

        except Exception as e:

            print(traceback.format_exc())


        return False



    def has_object_permission(self, request, view, obj):

        try:

            if request.user.is_anonymous:

                return False


            if getattr(view.get_obj_organization( obj = obj ), 'id', 'no-org-found') in view._user_organizations:

                return True


        except Exception as e:

            print(traceback.format_exc())

        return False
