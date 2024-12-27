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


            has_permission_required: bool = False

            if getattr(view, '_user_permissions', []):

                has_permission_required = view.get_permission_required() in getattr(view, '_user_permissions', [])



            if has_permission_required is True:

                if obj_organization is None:

                    return True

                elif obj_organization is not None:

                    if view.has_organization_permission(
                        organization = obj_organization.id,
                        permissions_required = [ view.get_permission_required() ]
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


            object_organization: int = getattr(view.get_obj_organization( obj = obj ), 'id', None)


            if object_organization:

                if(
                    object_organization
                    in view.get_permission_organizations( view.get_permission_required() )
                ):

                    return True


            elif not self.is_tenancy_model( view ):

                return True


        except Exception as e:

            print(traceback.format_exc())

        return False
