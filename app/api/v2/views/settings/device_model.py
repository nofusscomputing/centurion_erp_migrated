from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.v2.serializers.itam.device import ModelSerializer, ViewSerializer
from api.views.mixin import OrganizationPermissionAPI

from itam.models.device_models import DeviceModel



class ViewSet(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = DeviceModel.objects.all()

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer


        return ModelSerializer



    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    def list(self, request):

        return super().list(request)



    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)



    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.queryset.filter().order_by('name')

        else:

            return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



    def get_view_name(self):
        if self.detail:
            return "DeviceModel"
        
        return 'DeviceModel'
