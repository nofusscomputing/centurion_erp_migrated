from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.serializers.project_management.project_task import ProjectTaskSerializer

from api.views.core.tickets import View



@extend_schema(deprecated=True)
class View(View):

    _ticket_type:str = 'project_task'


    @extend_schema(
        summary='Create a Project Task',
        request = ProjectTaskSerializer,
        responses = {
            201: OpenApiResponse(
                response = ProjectTaskSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)



    @extend_schema(
        summary='Fetch all project tasks',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectTaskSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected project task',
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = ProjectTaskSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):

        if self.detail:
            return "Project Task"
        
        return 'Project Tasks'
