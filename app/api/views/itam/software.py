# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets

from itam.models.software import Software

from api.serializers.itam.software import SoftwareSerializer
from api.views.mixin import OrganizationPermissionAPI



class SoftwareViewSet(viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Software.objects.all()

    serializer_class = SoftwareSerializer


    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Software, pk=item)


    def get_queryset(self):
        return Software.objects.all()


    def get_view_name(self):
        return "Software"
