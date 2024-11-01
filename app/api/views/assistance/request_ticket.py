from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.serializers.assistance.request import RequestTicketSerializer
from api.views.core.tickets import View


@extend_schema(deprecated=True)
class View(View):

    _ticket_type:str = 'request'


    @extend_schema(
        summary='Create a ticket',
        description = """This model includes all of the ticket types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        request = RequestTicketSerializer,
        responses = {
            201: OpenApiResponse(
                response = RequestTicketSerializer,
            ),
        }
    )
    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)



    @extend_schema(
        summary='Fetch all tickets',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = RequestTicketSerializer
            )
        }
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Fetch the selected ticket',
        description = """This model includes all of the ticket comment types. 
        Due to this not all fields will be available and what fields are available
        depends upon the comment type. see
        [administration docs](https://nofusscomputing.com/projects/centurion_erp/administration/core/ticketing/index.html) for more info.
        """,
        methods=["GET"],
        responses = {
            200: OpenApiResponse(
                description='Success',
                response = RequestTicketSerializer
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)


    def get_view_name(self):

        if self.detail:
            return "Request Ticket"
        
        return 'Request Tickets'
