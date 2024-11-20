from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from rest_framework.fields import empty
from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI

from api.viewsets.common import ModelViewSet

from itam.serializers.device_operating_system import (
    DeviceOperatingSystem,
    DeviceOperatingSystemModelSerializer,
    DeviceOperatingSystemViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            201: OpenApiResponse(description='Device created', response=DeviceOperatingSystemModelSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device operating system',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device operating system',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        # 'action',
        # 'software__category',
        'organization',
        # 'software',
    ]

    search_fields = []

    model = DeviceOperatingSystem

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_description = 'Device Operating System'

    # allowed_methods = [
    #     'GET',
    #     'PATCH',
    #     'OPTIONS',
    #     'HEAD',
    # ]

    @property
    def allowed_methods(self):
        
        if len(list(self.get_queryset())) == 1:

            return [
                'GET',
                'PATCH',
                'OPTIONS',
                'HEAD',
            ]

        return [
                'GET',
                'PATCH',
                'POST',
                'OPTIONS',
                'HEAD',
            ]


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
