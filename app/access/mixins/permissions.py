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

    _is_tenancy_model: bool = None

    def is_tenancy_model(self, view) -> bool:
        """Determin if the Model is a `Tenancy` Model

        Will look at the model defined within the view unless a parent
        model is found. If the latter is true, the parent_model will be used to
        determin if the model is a `Tenancy` model

        Args:
            view (object): The View the HTTP request was mad to

        Returns:
            True (bool): Model is a Tenancy Model.
            False (bool): Model is not a Tenancy model.
        """

        if not self._is_tenancy_model:

            if hasattr(view, 'model'):

                self._is_tenancy_model = issubclass(view.model, TenancyObject)

                if view.get_parent_model():

                    self._is_tenancy_model = issubclass(view.get_parent_model(), TenancyObject)

        return self._is_tenancy_model



    def has_permission(self, request, view):
        """ Check if user has the required permission

        Permission flow is as follows:

        - Un-authenticated users. Access Denied

        - Authenticated user whom make a request using wrong method. Access
        Denied

        - Authenticated user who is not in same organization as object. Access
        Denied

        - Authenticated user who is in same organization as object, however is
        missing the correct permission. Access Denied

        Depending upon user type, they will recieve different feedback. In order
        they are: 

        - Non-authenticated users will **always** recieve HTTP/401

        - Authenticated users who use an unsupported method, HTTP/405

        - Authenticated users missing the correct permission recieve HTTP/403

        Args:
            request (object): The HTTP Request Object
            view (_type_): The View/Viewset Object the request was made to

        Raises:
            PermissionDenied: User does not have the required permission.
            NotAuthenticated: User is not logged into Centurion.
            ValueError: Could not determin the view action.

        Returns:
            True (bool): User has the required permission.
            False (bool): User does not have the required permission
        """

        if request.user.is_anonymous:

            raise centurion_exceptions.NotAuthenticated()

        try:


            view.get_user_organizations( request.user )

            has_permission_required: bool = False

            user_permissions = getattr(view, '_user_permissions', None)

            permission_required = view.get_permission_required()


            if permission_required and user_permissions:
                # No permission_required couldnt get permissions
                # No user_permissions, user missing the required permission

                has_permission_required: bool = permission_required in user_permissions


            if request.method not in view.allowed_methods:

                raise centurion_exceptions.MethodNotAllowed(method = request.method)


            elif not has_permission_required and not request.user.is_superuser:

                raise centurion_exceptions.PermissionDenied()


            obj_organization: Organization = view.get_obj_organization(
                request = request
            )

            view_action: str = None

            if(
                view.action == 'create'
                and request.method == 'POST'
            ):

                view_action = 'add'

            elif(
                view.action == 'destroy'
                and request.method == 'DELETE'
            ):

                view_action = 'delete'

                obj_organization: Organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif (
                view.action == 'list'
            ):

                view_action = 'view'

            elif (
                view.action == 'partial_update'
                and request.method == 'PATCH'
            ):

                view_action = 'change'

                obj_organization: Organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif (
                view.action == 'update'
                and request.method == 'PUT'
            ):

                view_action = 'change'

                obj_organization: Organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif(
                view.action == 'retrieve'
                and request.method == 'GET' 
            ):

                view_action = 'view'

                obj_organization: Organization = view.get_obj_organization(
                    obj = view.get_object()
                )

            elif(
                view.action == 'metadata'
                and request.method == 'OPTIONS'
            ):

                return True


            if view_action is None:

                raise ValueError('view_action could not be defined.')


            if obj_organization is None or request.user.is_superuser:

                return True

            elif obj_organization is not None:

                if view.has_organization_permission(
                    organization = obj_organization.id,
                    permissions_required = [ view.get_permission_required() ]
                ):

                        return True


        except ValueError as e:

            # ToDo: This exception could be used in traces as it provides
            # information as to dodgy requests. This exception is raised
            # when the method does not match the view action.

            print(traceback.format_exc())

        except centurion_exceptions.Http404 as e:
            # This exception genrally means that the user is not in the same
            # organization as the object as objects are filtered to users
            # organizations ONLY.

            pass

        except centurion_exceptions.ObjectDoesNotExist as e:
            # This exception genrally means that the user is not in the same
            # organization as the object as objects are filtered to users
            # organizations ONLY.

            pass

        except centurion_exceptions.PermissionDenied as e:
            # This Exception will be raised after this function has returned
            # False.

            pass


        return False


    def has_object_permission(self, request, view, obj):

        try:

            if request.user.is_anonymous:

                return False


            object_organization: int = getattr(view.get_obj_organization( obj = obj ), 'id', None)

            if object_organization:

                if(
                    object_organization
                    in view.get_permission_organizations( view.get_permission_required() )
                    or request.user.is_superuser
                    or getattr(self.request.app_settings.global_organization, 'id', 0) == int(object_organization)
                ):

                    return True


            elif not self.is_tenancy_model( view ) or request.user.is_superuser:

                return True


        except Exception as e:

            print(traceback.format_exc())

        return False
