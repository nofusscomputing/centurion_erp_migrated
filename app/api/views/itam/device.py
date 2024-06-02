from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.itam.device import DeviceSerializer
from api.views.mixin import OrganizationPermissionAPI

from itam.models.device import Device



class DeviceViewSet(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Device.objects.all()

    serializer_class = DeviceSerializer


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.queryset.filter().order_by('name')

        else:

            return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')


    def get_view_name(self):
        return "Device"
