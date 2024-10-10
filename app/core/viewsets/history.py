from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.views.mixin import OrganizationPermissionAPI

from core.serializers.history import (
    History,
    HistoryModelSerializer as ModelSerializer,
    HistoryViewSerializer as ViewSerializer
)

from api.v2.views.metadata import NavigationMetadata



class ViewSet(OrganizationMixin, viewsets.ModelViewSet):

    allowed_methods = [
        'GET',
        'OPTIONS'
    ]

    filterset_fields = [
        'item_parent_pk',
        'item_parent_class'
    ]


    model = History

    metadata_class = NavigationMetadata

    permission_classes = [
        OrganizationPermissionAPI
    ]

    # queryset = History.objects.filter()

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer


        return ModelSerializer


    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        self.queryset = self.model.objects.filter(
            item_parent_class = self.kwargs['model_class'],
            item_parent_pk = self.kwargs['model_id']
        ).order_by('-created')

        return self.queryset

    def get_view_name(self):
        if self.detail:
            return "Device Note"
        
        return 'Device History'
