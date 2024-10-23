from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import viewsets

from access.mixin import OrganizationMixin

from api.serializers.project_management.project_type import ProjectType, ProjectTypeSerializer
from api.views.mixin import OrganizationPermissionAPI


@extend_schema(deprecated = True )
class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ProjectType.objects.all()

    serializer_class = ProjectTypeSerializer


    @extend_schema(
        summary='Create a project type',
        request = ProjectTypeSerializer,
        responses = {
            201: OpenApiResponse(
                response = ProjectTypeSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all project types',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectTypeSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected project type',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectTypeSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):

        if self.detail:
            return ProjectType._meta.verbose_name
        
        return ProjectType._meta.verbose_name_plural
