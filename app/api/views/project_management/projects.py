from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.serializers.project_management.projects import ProjectSerializer
from api.views.mixin import OrganizationPermissionAPI

from project_management.models.projects import Project



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    @extend_schema(
        summary = 'Create a project',
        methods=["POST"],
        responses = {
            201: OpenApiResponse(description='project created', response=ProjectSerializer),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema( summary='Fetch projects', methods=["GET"])
    def list(self, request):

        return super().list(request)


    @extend_schema( summary='Fetch the selected project', methods=["GET"])
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):
        if self.detail:
            return "Project"
        
        return 'Projects'
