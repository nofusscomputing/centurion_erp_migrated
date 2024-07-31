from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import generics

from api.serializers.config import ConfigGroupsSerializer
from api.views.mixin import OrganizationPermissionAPI

from config_management.models.groups import ConfigGroups



@extend_schema_view(
    get=extend_schema(
        summary = "Fetch Config groups",
        description="Returns a list of Config Groups."
    ),
)
class ConfigGroupsList(generics.ListAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ConfigGroups.objects.all()
    lookup_field = 'pk'
    serializer_class = ConfigGroupsSerializer


    def get_view_name(self):
        return "Config Groups"



@extend_schema_view(
    get=extend_schema(
        summary = "Get A Config Group",
        # responses = {}
    ),
)
class ConfigGroupsDetail(generics.RetrieveAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ConfigGroups.objects.all()
    lookup_field = 'pk'
    serializer_class = ConfigGroupsSerializer


    def get_view_name(self):
        return "Config Group"


