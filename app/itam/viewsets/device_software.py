from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.fields import empty
from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI

from api.viewsets.common import ModelViewSet

from itam.serializers.device_software import (
    DeviceSoftware,
    DeviceSoftwareModelSerializer,
    DeviceSoftwareViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add device software',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=DeviceSoftwareModelSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device software',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all device software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device software',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        'action',
        'software__category',
        'organization',
        'software',
    ]

    search_fields = [
        'name',
    ]

    model = DeviceSoftware

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_description = 'Device Models'


    def get_queryset(self):

        queryset = super().get_queryset()

        queryset = queryset.filter(device_id=self.kwargs['device_id'])

        self.queryset = queryset

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']
