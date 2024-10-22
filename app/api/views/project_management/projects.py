from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest, PolymorphicProxySerializer

from rest_framework import generics, viewsets
from rest_framework.response import Response

from access.mixin import OrganizationMixin

from api.serializers.project_management.projects import ProjectSerializer, ProjectImportSerializer
from api.views.mixin import OrganizationPermissionAPI

from project_management.models.projects import Project

from settings.models.user_settings import UserSettings


@extend_schema(deprecated = True )
class View(OrganizationMixin, viewsets.ModelViewSet):

    filterset_fields = [
        'external_system',
        'external_ref',
    ]

    search_fields = [
        'name',
        'description',
    ]

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = Project.objects.all()

    # serializer_class = ProjectSerializer

    def get_serializer_class(self):

        if self.has_organization_permission(
            organization = UserSettings.objects.get(user = self.request.user).default_organization,
            permissions_required = ['project_management.import_project']
        ) or self.request.user.is_superuser:

            return ProjectImportSerializer

        return ProjectSerializer

    @extend_schema(
        summary = 'Create a project',
        description = """**Note:** Users whom lack permssion `import_project`,
        will be unable to add, edit and view fields: `created`, `external_ref`, `external_system`,
        and `is_deleted`.
        """,
        methods=["POST"],
        request = ProjectImportSerializer,
        responses = {
            201: OpenApiResponse(description='project created', response=ProjectImportSerializer),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch projects',
        description = """**Note:** Users whom lack permssion `import_project`,
        will be unable to add, edit and view fields: `created`, `external_ref`, `external_system`,
        and `is_deleted`.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='projects', response=ProjectImportSerializer)
        }
    )
    def list(self, request):

        return super().list(request)


    @extend_schema(
        summary='Fetch the selected project',
        description = """**Note:** Users whom lack permssion `import_project`,
        will be unable to add, edit and view fields: `created`, `external_ref`, `external_system`,
        and `is_deleted`.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(description='projects', response=ProjectImportSerializer)
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.queryset.filter()

        else:

            return self.queryset.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True))


    def get_view_name(self):
        if self.detail:
            return "Project"
        
        return 'Projects'
