from django.contrib.auth.models import Permission

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework import generics, routers, serializers, views
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response

from access.mixin import OrganizationMixin
from access.models import Organization, Team

from api.serializers.access import OrganizationSerializer, OrganizationListSerializer, TeamSerializer, TeamPermissionSerializer
from api.views.mixin import OrganizationPermissionAPI


@extend_schema_view(
    get=extend_schema(
        summary = "Fetch Organizations",
        description="Returns a list of organizations."
    ),
)
class OrganizationList(generics.ListAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Organization.objects.all()
    lookup_field = 'pk'
    serializer_class = OrganizationListSerializer


    def get_view_name(self):
        return "Organizations"



@extend_schema_view(
    get=extend_schema(
        summary = "Get An Organization",
    ),
    patch=extend_schema(
        summary = "Update an organization",
    ),
    put=extend_schema(
        summary = "Update an organization",
    ),
)
class OrganizationDetail(generics.RetrieveUpdateAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Organization.objects.all()
    lookup_field = 'pk'
    serializer_class = OrganizationSerializer


    def get_view_name(self):
        return "Organization"



@extend_schema_view(
    post=extend_schema(
        summary = "Create a Team",
        description = """Create a team within the defined organization.""",
        tags = ['team',],
        request = TeamSerializer,
        responses = {
            200: OpenApiResponse(description='Team has been updated with the supplied permissions'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
        }
    ),
    create=extend_schema(exclude=True),
)
class TeamList(generics.ListCreateAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


    def get_queryset(self):

        self.queryset = Team.objects.filter(organization=self.kwargs['organization_id'])

        return self.queryset


    def get_view_name(self):
        return "Organization Teams"



@extend_schema_view(
    get=extend_schema(
        summary = "Fetch a Team",
        description = """Fetch a team within the defined organization.
        """,
        methods=["GET"],
        tags = ['team',],
        request = TeamSerializer,
        responses = {
            200: OpenApiResponse(description='Team has been updated with the supplied permissions'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
        }
    ),
    patch=extend_schema(
        summary = "Update a Team",
        description = """Update a team within the defined organization.
        """,
        methods=["Patch"],
        tags = ['team',],
        request = TeamSerializer,
        responses = {
            200: OpenApiResponse(description='Team has been updated with the supplied permissions'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
        }
    ),
    put = extend_schema(
        summary = "Amend a team",
        tags = ['team',],
    ),
    delete=extend_schema(
        summary = "Delete a Team",
        tags = ['team',],
    ),
    post = extend_schema(
        exclude = True,
    )
)
class TeamDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    lookup_field = 'group_ptr_id'



@extend_schema_view(
    get=extend_schema(
        summary = "Fetch a teams permissions",
        tags = ['team',],
    ),
    post=extend_schema(
        summary = "Replace team Permissions",
        description = """Replace the teams permissions with the permissions supplied.

Teams Permissions will be replaced with the permissions supplied. **ALL** existing permissions will be
removed.

permissions are required to be in format `<module name>_<permission>_<table name>`
        """,

        methods=["POST"],
        tags = ['team',],
        request = TeamPermissionSerializer,
        responses = {
            200: OpenApiResponse(description='Team has been updated with the supplied permissions'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
        }
    ),
    delete=extend_schema(
        summary = "Delete permissions",
        tags = ['team',],
    ),
    patch = extend_schema(
        summary = "Amend team Permissions",
        description = """Amend the teams permissions with the permissions supplied.

Teams permissions will include the existing permissions along with the ones supplied.
permissions are required to be in format `<module name>_<permission>_<table name>`
        """,

        methods=["PATCH"],
        parameters = None,
        tags = ['team',],
        request = TeamPermissionSerializer,
        responses = {
            200: OpenApiResponse(description='Team has been updated with the supplied permissions'),
            401: OpenApiResponse(description='User Not logged in'),
            403: OpenApiResponse(description='User is missing permission or in different organization'),
        }
    ),
    put = extend_schema(
        summary = "Amend team Permissions",
        tags = ['team',],
    )
)
class TeamPermissionDetail(views.APIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Team.objects.all()

    serializer_class = TeamPermissionSerializer


    def get(self, request, *args, **kwargs):

        return Response(data=Team.objects.get(pk=self.kwargs['group_ptr_id']).permission_list()[0])


    def get_view_name(self):
        return "Team Permissions"


    def delete(self, request, *args, **kwargs):

        vals = self.process_request()

        remove = vals['remove']

        new_permission = Team.objects.get(pk=self.kwargs['group_ptr_id'])


        for remove_permission in remove:
            new_permission.permissions.remove(remove_permission)
            new_permission.save()

        return Response(data=Team.objects.get(pk=self.kwargs['group_ptr_id']).permission_list()[0])


    def patch(self, request, *args, **kwargs):

        vals = self.process_request()

        add = vals['add']

        new_permission = Team.objects.get(pk=self.kwargs['group_ptr_id'])

        for add_permission in add:
            new_permission.permissions.add(add_permission)
            new_permission.save()


        return Response(data=Team.objects.get(pk=self.kwargs['group_ptr_id']).permission_list()[0])


    def post(self, request, *args, **kwargs):

        vals = self.process_request()

        add = vals['add']
        remove = vals['remove']
        exists = vals['exists']

        new_permission = Team.objects.get(pk=self.kwargs['group_ptr_id'])

        for add_permission in add:
            new_permission.permissions.add(add_permission)
            new_permission.save()

        for remove_permission in remove:
            new_permission.permissions.remove(remove_permission)
            new_permission.save()


        return Response(data=Team.objects.get(pk=self.kwargs['group_ptr_id']).permission_list()[0])


    def process_request(self) -> dict({
        "add": list,
        "remove": list,
        "exists": list
    }):

        initial_values = Team.objects.get(pk=self.kwargs['group_ptr_id']).permission_list()

        add = []
        remove = []
        exists = []


        for request_permission in self.request.data:

            fields = request_permission.split('.')

            try:

                permission = Permission.objects.get(codename=str(fields[1]), content_type__app_label=str(fields[0]))

                exists += [ permission.id ]

                if permission and request_permission not in initial_values[0]:
                    add += [ permission.id ]

            except:

                raise serializers.ValidationError(f'Value was invalid: {request_permission}')

        for existing_permission in initial_values[1].all():

            if existing_permission.id not in add and existing_permission.id not in exists:
                remove += [ existing_permission.id ] 

        return {
            "add": add,
            "remove": remove,
            "exists": exists
        }
