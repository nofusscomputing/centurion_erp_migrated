from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from itam.models.device import Device

from rest_framework import views
from rest_framework.response import Response


class View(views.APIView):

    def get(self, request, slug):

        device = Device.objects.get(slug=slug)

        return Response(device.get_configuration(device.id))


    def get_view_name(self):
        return "Device Config"
