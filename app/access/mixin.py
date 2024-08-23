
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property

from .models import Organization, Team


class OrganizationMixin():
    """Base Organization class"""

    request = None

    user_groups = []


    def get_parent_obj(self):
        """ Get the Parent Model Object

        Use in views where the the model has no organization and the organization should be fetched from the parent model.

        Requires attribute `parent_model` within the view with the value of the parent's model class

        Returns:
            parent_model (Model): with PK from kwargs['pk']
        """

        return self.parent_model.objects.get(pk=self.kwargs['pk'])


    def object_organization(self) -> int:

        id = None

        try:

            if hasattr(self, 'get_queryset'):
                self.get_queryset()


            if hasattr(self, 'parent_model'):
                obj = self.get_parent_obj()

                id = obj.get_organization().id

                if obj.is_global:

                    id = 0


            if hasattr(self, 'get_object') and id is None:

                obj = self.get_object()

                id = obj.get_organization().id

                if hasattr(obj, 'is_global'):

                    if obj.is_global:

                        id = 0


        except AttributeError:

            if self.request.method == 'POST':

                if self.request.POST.get("organization", ""):

                    id = int(self.request.POST.get("organization", ""))

                for field in self.request.POST.dict(): # cater for fields prefixed '<prefix>-<field name>'

                    a_field = str(field).split('-')

                    if len(a_field) == 2:

                        if a_field[1] == 'organization':

                            id = int(self.request.POST.get(field))

        except:

            pass


        return id


    def is_member(self, organization: int) -> bool:
        """Returns true if the current user is a member of the organization

        iterates over the user_organizations list and returns true if the user is a member

        Returns:
            bool: _description_
        """

        is_member = False

        if organization in self.user_organizations():

            return True

        return is_member


    def get_permission_required(self):
        """
        Override of 'PermissionRequiredMixin' method so that this mixin can obtain the required permission.
        """

        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms


    @cached_property
    def is_manager(self) -> bool:
        """ Returns true if the current user is a member of the organization"""
        is_manager = False

        return is_manager


    def user_organizations(self) -> list():
        """Current Users organizations

        Fetches the Organizations the user is apart of.

        Get All groups the user is part of, fetch the associated team,
        iterate over the results adding the organization ID to a list to be returned.

        Returns:
            _type_: User Organizations.
        """

        user_organizations = []

        teams = Team.objects

        for group in self.request.user.groups.all():

            team = teams.get(pk=group.id)

            self.user_groups = self.user_groups + [group.id]

            user_organizations = user_organizations + [team.organization.id]

        return user_organizations


    # ToDo: Ensure that the group has access to item
    def has_organization_permission(self, organization: int=None) -> bool:

        has_permission = False

        if not organization:

            organization = self.object_organization()

        if self.is_member(organization) or organization == 0:

            groups = Group.objects.filter(pk__in=self.user_groups)

            for group in groups:

                team = Team.objects.filter(pk=group.id)
                team = team.values('organization_id').get()

                for permission in group.permissions.values('content_type__app_label', 'codename').all():

                    assembled_permission = str(permission["content_type__app_label"]) + '.' + str(permission["codename"])

                    if assembled_permission in self.get_permission_required() and (team['organization_id'] == organization or organization == 0):

                        return True

        return has_permission


    def permission_check(self, request, permissions_required: list = None) -> bool:

        self.request = request

        if permissions_required:

            self.permission_required = permissions_required

        organization_manager_models = [
            'access.organization',
            'access.team',
            'access.teamusers',
        ]

        is_organization_manager = False

        queryset = None

        if hasattr(self, 'get_queryset'):

            queryset = self.get_queryset()

        obj = None

        if hasattr(self, 'get_object'):


            try:

                obj = self.get_object()

            except:

                pass


            if hasattr(self, 'model'):

                if self.model._meta.label_lower in organization_manager_models:

                    organization = Organization.objects.get(pk=self.object_organization())

                    if organization.manager == request.user:

                        is_organization_manager = True

                        return True


        if request.user.is_superuser:

            return True

        perms = self.get_permission_required()

        if self.has_organization_permission():

            return True

        if self.request.user.has_perms(perms) and len(self.kwargs) == 0 and str(self.request.method).lower() == 'get':

            return True

        for required_permission in self.permission_required:

            if required_permission.replace(
                    'view_', ''
                ) == 'access.organization' and len(self.kwargs) == 0:

                return True

        return False



class OrganizationPermission(AccessMixin, OrganizationMixin):
    """## Permission Checking
    
    The base django permissions have not been modified with this app providing Multi-Tenancy. This is done by a mixin, that checks if the item is apart of an organization, if it is; confirmation is made that the user is part of the same organization and as long as they have the correct permission within the organization, access is granted.


    ### How it works

    The overall permissions system of django has not been modified with it remaining fully functional. The multi-tenancy has been setup based off of an organization with teams. A team to the underlying django system is an extension of the django auth group and for every team created a django auth group is created. THe group name is set using the following format: `<organization>_<team name>` and contains underscores `_` instead of spaces.

    A User who is added to an team as a "Manager" can modify the team members or if they have permission `access.change_team` which also allows the changing of team permissions. Modification of an organization can be done by the django administrator (super user) or any user with permission `access._change_organization`.

    Items can be set as `Global`, meaning that all users who have the correct permission regardless of organization will be able to take action against the object.

    Permissions that can be modified for a team have been limited to application permissions only unless adjust the permissions from the django admin site.


    ### Multi-Tenancy workflow

    The workflow is conducted as part of the view and has the following flow:

    1. Checks if user is member of organization the object the action is being performed on. Will also return true if the object has field `is_global` set to `true`.

    1. Fetches all teams the user is part of.

    1. obtains all permissions that are linked to the team.

    1. checks if user has the required permission for the action.

    1. confirms that the team the permission came from is part of the same organization as the object the action is being conducted on.

    1. ONLY on success of the above items, grants access.
    """

    permission_required: list = []
    """ Permission required for the view

    Not specifying this property adjusts the permission check logic so that you can
    use the `permission_check()` function directly.

    An example of a get request....

    ``` py
    def get(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:

                return self.handle_no_permission()

        if not self.permission_check(request, [ 'access.view_organization' ]):

            raise PermissionDenied('You are not part of this organization')

        return super().get(request, *args, **kwargs)
    ```
    this example details manual usage of the `permission_check()` function for a get request.
    """


    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
                return self.handle_no_permission()
        
        if len(self.permission_required) > 0:

            non_organization_models = [
                'TaskResult'
            ]

            if hasattr(self, 'model'):

                
                if hasattr(self.model, '__name__'):

                    if self.model.__name__ in non_organization_models:

                        if hasattr(self, 'get_object'):

                            self.get_object()

                        perms = self.get_permission_required()


                        if not self.request.user.has_perms(perms):

                            return self.handle_no_permission()

                        return super().dispatch(self.request, *args, **kwargs)


            if not self.permission_check(request):

                raise PermissionDenied('You are not part of this organization')

        return super().dispatch(self.request, *args, **kwargs)
