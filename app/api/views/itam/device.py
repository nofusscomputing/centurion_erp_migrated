# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets

from itam.models.device import Device

from api.serializers.itam.device import DeviceSerializer
from api.views.mixin import OrganizationPermissionAPI


class DeviceViewSet(viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Device.objects.all()

    serializer_class = DeviceSerializer

    def get_view_name(self):
        return "Device"
