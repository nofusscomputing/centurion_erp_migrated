from django.contrib.auth.models import User, Group
from access.models import Organization, Team


class OrganizationMixin:
    """Organization Tenancy Mixin

    This class is intended to be included in **ALL** View / Viewset classes as
    it contains the functions/methods required to conduct the permission
    checking.
    """


    _obj_organization: int = None
    """Cached Object Organization"""

    def get_obj_organization(self, obj = None, request = None) -> Organization:
        """Fetch the objects Organization

        Args:
            obj (Model): Model of object

        Raises:
            ValueError: When `obj` and `request` are both missing

        Returns:
            Organization: Organization the object is from
            None: No Organization was found
        """

        if obj is None and request is None:

            raise ValueError('Missing Parameter. obj or request must be supplied')

        
        if self._obj_organization:

            return self._obj_organization


        _obj_organization: Organization = None


        if obj:

            _obj_organization = getattr(obj, 'organization', None)


            if not _obj_organization:

                _obj_organization = getattr(obj, 'get_organization', lambda: None)()

        elif request:

            if getattr(request.stream, 'method', '') != 'DELETE':

                data = getattr(request, 'data', None)

                if data:

                    data_organization = self.kwargs.get('organization_id', None)

                    if not data_organization:

                        data_organization = request.data.get('organization_id', None)


                    if not data_organization:

                        data_organization = request.data.get('organization', None)


                    if data_organization:

                        _obj_organization = Organization.objects.get(
                            pk = int( data_organization )
                        )


        if self.get_parent_model():    # if defined is to overwrite object organization

            parent_obj = self.get_parent_obj()

            _obj_organization = parent_obj.get_organization()



        if _obj_organization:

            self._obj_organization = _obj_organization

        return self._obj_organization



    def get_parent_model(self):
        """Get the Parent Model

        This function exists so that dynamic parent models can be defined.
        They are defined by overriding this method.

        Returns:
            Model: Parent Model
        """

        return self.parent_model



    def get_parent_obj(self):
        """ Get the Parent Model Object

        Use in views where the the model has no organization and the organization should be fetched from the parent model.

        Requires attribute `parent_model` within the view with the value of the parent's model class

        Returns:
            parent_model (Model): with PK from kwargs['pk']
        """

        return self.parent_model.objects.get(pk=self.kwargs[self.parent_model_pk_kwarg])



    def get_permission_organizations(self, permission: str ) -> list([ int ]):
        """Return Organization(s) the permission belongs to

        Searches the users organizations for the required permission, if found
        the organization is added to the list to return.

        Args:
            permission (str): Permission to search users organizations for

        Returns:
            Organizations (list): All Organizations where the permission was found.
        """

        _permission_organizations: list = []

        for team in self.get_user_teams( self.request.user ):

            for team_permission in team.permissions.all():

                permission_value = str( team_permission.content_type.app_label + '.' + team_permission.codename )

                if permission_value == permission:

                    _permission_organizations += [ team.organization.id ]


        return _permission_organizations



    def get_permission_required(self) -> str:
        """ Get / Generate Permission Required

        If there is a requirement that there be custom/dynamic permissions,
        this function can be safely overridden.

        Raises:
            ValueError: Unable to determin the view action

        Returns:
            str: Permission in format `<app_name>.<action>_<model_name>`
        """


        view_action: str = None

        if(
            self.action == 'create'
            or getattr(self.request._stream, 'method', '') == 'POST'
        ):

            view_action = 'add'

        elif (
            self.action == 'partial_update'
            or self.action == 'update'
            or getattr(self.request._stream, 'method', '') == 'PATCH'
            or getattr(self.request._stream, 'method', '') == 'PUT'
        ):

            view_action = 'change'

        elif(
            self.action == 'destroy'
            or getattr(self.request._stream, 'method', '') == 'DELETE'
        ):

            view_action = 'delete'

        elif (
            self.action == 'list'
        ):

            view_action = 'view'

        elif self.action == 'retrieve':

            view_action = 'view'



        if view_action is None:

            raise ValueError('view_action could not be defined.')


        permission = self.model._meta.app_label + '.' + view_action + '_' + self.model._meta.model_name

        permission_required = permission


        self.permission_required = permission_required

        return self.permission_required



    parent_model: str = None
    """ Parent Model

    This attribute defines the parent model for the model in question. The parent model when defined
    will be used as the object to obtain the permissions from.
    """


    parent_model_pk_kwarg: str = 'pk'
    """Parent Model kwarg

    This value is used to define the kwarg that is used as the parent objects primary key (pk).
    """


    _user_organizations: list = None
    """Cached User Organizations"""


    _user_teams: list = None
    """Cached User Teams"""


    _user_permissions: list = None
    """Cached User User Permissions"""


    def get_user_organizations(self, user: User) -> list([int]):
        """Get the Organization the user is a part of

        Args:
            user (User): User Making the request

        Returns:
            list(int()): List containing the organizations the user is a part of.
        """

        if self._user_organizations and self._user_teams and self._user_permissions:

            return self._user_organizations


        teams = Team.objects.all()

        _user_organizations: list([ int ]) = []

        _user_teams: list([ Team ]) = []

        _user_permissions: list([ str ]) = []

        for group in user.groups.all():

            team = teams.get(pk=group.id)

            if team not in _user_teams:

                _user_teams += [ team ]

                for permission in team.permissions.all():

                    permission_value = str( permission.content_type.app_label + '.' + permission.codename )

                    if permission_value not in _user_permissions:

                        _user_permissions += [ permission_value ]


            if team.organization.id not in _user_organizations:

                _user_organizations += [ team.organization.id ]


        if len(_user_organizations) > 0:

            self._user_organizations = _user_organizations

        if len(_user_teams) > 0:

            self._user_teams = _user_teams

        if len(_user_permissions) > 0:

            self._user_permissions = _user_permissions


        return self._user_organizations



    def get_user_teams(self, user: User) -> list([ Team ]):

        if not self._user_teams:

            self.get_user_organizations( user = user )

        return self._user_teams



    def has_organization_permission(self, organization: int, permissions_required: list) -> bool:
        """ Check if user has permission within organization.

        Args:
            organization (int): Organization to check.
            permissions_required (list): if doing object level permissions, pass in required permission.

        Returns:
            bool: True for yes.
        """

        has_permission: bool = False

        for team in self.get_user_teams( user = self.request.user ):

            if team.organization.id == int(organization):

                for permission in team.permissions.all():

                    assembled_permission = str(permission.content_type.app_label) + '.' + str( permission.codename )

                    if assembled_permission in permissions_required:

                        has_permission = True


        return has_permission



    def is_member(self, organization: int) -> bool:
        """Returns true if the current user is a member of the organization

        iterates over the user_organizations list and returns true if the user is a member

        Returns:
            bool: _description_
        """

        is_member: bool = False

        if organization is None:

            return False

        if int(organization) in self.get_user_organizations(self.request.user):

            is_member = True

        return is_member
