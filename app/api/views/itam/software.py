# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework import generics

from itam.models.software import Software
from api.serializers.itam.software import SoftwareSerializer


class List(generics.ListCreateAPIView):
    permission_required = 'itam.view_software'
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

    def get_view_name(self):
        return "Softwares"


class Detail(generics.RetrieveUpdateDestroyAPIView):
    permission_required = 'itam.view_software'
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

    def get_view_name(self):
        return "Software"
