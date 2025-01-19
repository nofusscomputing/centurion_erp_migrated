from django.contrib.auth.middleware import (
    AuthenticationMiddleware,
    SimpleLazyObject,
    partial,
)
from django.contrib.auth.models import User, Group
from django.utils.deprecation import MiddlewareMixin

from access.models import Organization, Team

from settings.models.app_settings import AppSettings


class RequestTenancy(MiddlewareMixin):
    """Access Middleware

    Serves the purpose of adding the users tenancy details to rhe request
    object.
    """


    def process_request(self, request):

        request.app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )

        request.tenancy = Tenancy(user = request.user, app_settings = request.app_settings)



class Tenancy:

    user: User = None

    groups: list([Group]) = None

    _app_settings: AppSettings = None


    _user_organizations: list([Organization]) = None
    """Cached User Organizations"""

    _user_teams: list([Team]) = None
    """Cached User Teams"""


    _user_permissions: list([str]) = None
    """Cached User User Permissions"""



    def __init__(self, user: User, app_settings: AppSettings):

        self.user = user

        self. _app_settings = app_settings

        self.groups = user.groups.select_related('team', 'team__organization').prefetch_related('team__permissions__content_type')

        self._user_organizations = []

        self._user_groups = []

        self._user_teams = []

        self._user_permissions = []


        for group in self.groups:

            if group.team not in self._user_teams:

                self._user_teams += [ group.team ]

                for permission in group.team.permissions.all():

                    permission_value = str( permission.content_type.app_label + '.' + permission.codename )

                    if permission_value not in self._user_permissions:

                        self._user_permissions += [ permission_value ]


            if group.team.organization not in self._user_organizations:

                self._user_organizations += [ group.team.organization ]



    def is_member(self, organization: Organization) -> bool:
        """Returns true if the current user is a member of the organization

        iterates over the user_organizations list and returns true if the user is a member

        Returns:
            bool: _description_
        """

        is_member: bool = False

        if organization is None:

            return False

        if int(organization) in self._user_organizations:

            is_member = True

        return is_member



    def has_organization_permission(self, organization: Organization, permissions_required: str) -> bool:
        """ Check if user has permission within organization.

        Args:
            organization (int): Organization to check.
            permissions_required (list): if doing object level permissions, pass in required permission.

        Returns:
            bool: True for yes.
        """

        has_permission: bool = False

        if type(organization) is not Organization:

            raise TypeError('Organization must be of type Organization')


        if type(permissions_required) is not str:

            raise TypeError('permissions_required must be of type str')


        if not organization:

            return has_permission


        for team in self._user_teams:

            if(
                team.organization.id == int(organization)
                or getattr(self._app_settings.global_organization, 'id', 0) == int(organization)
            ):

                for permission in team.permissions.all():

                    assembled_permission = str(permission.content_type.app_label) + '.' + str( permission.codename )

                    if assembled_permission == permissions_required:

                        has_permission = True


        return has_permission
