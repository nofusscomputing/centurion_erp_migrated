from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from settings.serializers.external_links import ExternalLink, ExternalLinkModelSerializer, ExternalLinkViewSerializer
from api.views.mixin import OrganizationPermissionAPI

# from settings.models.external_link import ExternalLink



class ViewSet(OrganizationMixin, viewsets.ModelViewSet):

    filterset_fields = [
        'devices',
        'software',
    ]

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ExternalLink.objects.all()

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ExternalLinkViewSerializer


        return ExternalLinkModelSerializer



    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    def list(self, request):

        return super().list(request)



    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)



    # def get_queryset(self):

    #     if self.request.user.is_superuser:

    #         return self.queryset.filter().order_by('name')

    #     else:

    #         return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



    def get_view_name(self):
        if self.detail:
            return "External Link"
        
        return 'External Links'
