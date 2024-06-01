# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework import generics

from itam.models.software import Software

from api.serializers.itam.software import SoftwareSerializer
from api.views.mixin import OrganizationPermissionAPI

class List(generics.ListCreateAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

    def get_view_name(self):
        return "Softwares"


class Detail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

    def get_view_name(self):
        return "Software"
