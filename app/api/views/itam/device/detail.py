# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework import generics

from itam.models.device import Device

from api.serializers.itam.device import DeviceSerializer
from api.views.mixin import OrganizationPermissionAPI

class List(generics.ListCreateAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_view_name(self):
        return "Devices"


class Detail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Device.objects.all()

    serializer_class = DeviceSerializer

    def get_view_name(self):
        return "Device"
