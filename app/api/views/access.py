from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework import generics

from access.models import Organization, Team
from api.serializers.access import OrganizationSerializer, TeamSerializer



class OrganizationList(PermissionRequiredMixin, LoginRequiredMixin, generics.ListCreateAPIView):
    permission_required = 'access.view_organization'
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


    def get_view_name(self):
        return "Organizations"



class OrganizationDetail(PermissionRequiredMixin, LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_required = 'access.view_organization'
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


    def get_view_name(self):
        return "Organization"



class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer



class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    lookup_field = 'group_ptr_id'
