from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import viewsets

from access.mixin import OrganizationMixin

from api.serializers.project_management.project_state import ProjectState, ProjectStateSerializer
from api.views.core.tickets import View
from api.views.mixin import OrganizationPermissionAPI


@extend_schema(deprecated = True )
class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ProjectState.objects.all()

    serializer_class = ProjectStateSerializer


    @extend_schema(
        summary='Create a project state',
        request = ProjectStateSerializer,
        responses = {
            201: OpenApiResponse(
                response = ProjectStateSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all project states',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectStateSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected project state',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectStateSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):

        if self.detail:
            return ProjectState._meta.verbose_name
        
        return ProjectState._meta.verbose_name_plural
