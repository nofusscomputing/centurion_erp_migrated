from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets

from api.serializers.itam.software import SoftwareSerializer
from api.views.mixin import OrganizationPermissionAPI

from itam.models.software import Software



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

        if self.request.user.is_superuser:

            return self.queryset.filter().order_by('name')

        else:

            return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')


    def get_view_name(self):
        return "Software"
