
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property



from .models import Team


class OrganizationMixin():
    """Base Organization class"""

    request = None

    user_groups = []

    def object_organization(self) -> int:

        id = None

        try:

            if hasattr(self, 'get_queryset'):
                self.get_queryset()


            if hasattr(self, 'get_object'):

                obj = self.get_object()

                id = obj.get_organization().id

                if obj.is_global:

                    id = 0


        except AttributeError:

            if self.request.method == 'POST':

                if self.request.POST.get("organization", ""):

                    id = int(self.request.POST.get("organization", ""))

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

        Args:
            request (_type_): Current http request

        Returns:
            _type_: _description_
        """

        user_organizations = []

        teams = Team.objects

        for group in self.request.user.groups.all():

            team = teams.get(pk=group.id)

            self.user_groups = self.user_groups + [group.id]

            user_organizations = user_organizations + [team.organization.id]

        return user_organizations


    # ToDo: Ensure that the group has access to item
    def has_organization_permission(self, organization=None) -> bool:

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



class OrganizationPermission(AccessMixin, OrganizationMixin):
    """checking organization membership"""


    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if not request.user.is_authenticated:
                return self.handle_no_permission()

        if hasattr(self, 'get_object'):

            if not self.has_organization_permission() and not request.user.is_superuser:
                raise PermissionDenied('You are not part of this organization')

        return super().dispatch(self.request, *args, **kwargs)
