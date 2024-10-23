from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import viewsets

from access.mixin import OrganizationMixin

from api.serializers.project_management.project_milestone import ProjectMilestone, ProjectMilestoneSerializer
# from api.views.core.tickets import View
from api.views.mixin import OrganizationPermissionAPI


@extend_schema(deprecated = True )
class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    queryset = ProjectMilestone.objects.all()

    serializer_class = ProjectMilestoneSerializer


    @extend_schema(
        summary='Create a project milestone',
        request = ProjectMilestoneSerializer,
        responses = {
            201: OpenApiResponse(
                response = ProjectMilestoneSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch all project milestones',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectMilestoneSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected project milestone',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectMilestoneSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):

        if self.detail:
            return ProjectMilestone._meta.verbose_name
        
        return ProjectMilestone._meta.verbose_name_plural


    def get_queryset(self):

        if 'project_id' in self.kwargs:

            self.queryset = self.queryset.filter(
                project=self.kwargs['project_id']
            )

        if 'pk' in self.kwargs:

            self.queryset = self.queryset.filter(
                pk = self.kwargs['pk']
            )

        return self.queryset
