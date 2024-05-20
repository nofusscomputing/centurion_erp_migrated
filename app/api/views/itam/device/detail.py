# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework import generics

from itam.models.device import Device
from api.serializers.itam.device import DeviceSerializer


class List(generics.ListCreateAPIView):
    permission_required = 'itam.view_device'
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_view_name(self):
        return "Devices"


class Detail(generics.RetrieveUpdateDestroyAPIView):
    permission_required = 'itam.view_device'
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_view_name(self):
        return "Device"
