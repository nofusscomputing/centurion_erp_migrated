from django.db.models import Q

from rest_framework import generics, viewsets

from access.mixin import OrganizationMixin

from api.serializers.assistance.request import RequestTicketSerializer
from api.serializers.itim.change import ChangeTicketSerializer
from api.serializers.itim.incident import IncidentTicketSerializer
from api.serializers.itim.problem import ProblemTicketSerializer
from api.serializers.project_management.project_task import ProjectTaskSerializer
from api.views.mixin import OrganizationPermissionAPI

from core.models.ticket import Ticket



class View(OrganizationMixin, viewsets.ModelViewSet):

    permission_classes = [
        OrganizationPermissionAPI
    ]

    def get_dynamic_permissions(self):

        if self.action == 'create':

            action_keyword = 'add'

        elif self.action == 'destroy':

            action_keyword = 'delete'

        elif self.action == 'list':

            action_keyword = 'view'

        elif self.action == 'partial_update':

            action_keyword = 'change'

        elif self.action == 'retrieve':

            action_keyword = 'view'

        elif self.action == 'update':

            action_keyword = 'change'

        elif self.action is None:

            action_keyword = 'view'

        else:

            raise ValueError('unable to determin the action_keyword')

        self.permission_required = [
            'core.' + action_keyword + '_ticket_' + self._ticket_type,
        ]

        return super().get_permission_required()


    queryset = Ticket.objects.all()


    def get_serializer(self, *args, **kwargs):

        if self._ticket_type == 'change':
            
            self.serializer_class = ChangeTicketSerializer

            self._ticket_type_value = Ticket.TicketType.CHANGE.value

        elif self._ticket_type == 'incident':
            
            self.serializer_class = IncidentTicketSerializer
            self._ticket_type_value = Ticket.TicketType.INCIDENT.value

        elif self._ticket_type == 'problem':
            
            self.serializer_class = ProblemTicketSerializer
            self._ticket_type_value = Ticket.TicketType.PROBLEM.value

        elif self._ticket_type == 'request':
            
            self.serializer_class = RequestTicketSerializer
            self._ticket_type_value = Ticket.TicketType.REQUEST.value

        elif self._ticket_type == 'project_task':
            
            self.serializer_class = ProjectTaskSerializer
            self._ticket_type_value = Ticket.TicketType.PROJECT_TASK.value

        else:

            raise ValueError('unable to determin the serializer_class')

        return super().get_serializer(*args, **kwargs)


    def get_queryset(self):

        if self._ticket_type == 'change':

            ticket_type = self.queryset.model.TicketType.CHANGE.value

        elif self._ticket_type == 'incident':

            ticket_type = self.queryset.model.TicketType.INCIDENT.value

        elif self._ticket_type == 'problem':

            ticket_type = self.queryset.model.TicketType.PROBLEM.value

        elif self._ticket_type == 'request':

            ticket_type = self.queryset.model.TicketType.REQUEST.value

        elif self._ticket_type == 'project_task':

            ticket_type = self.queryset.model.TicketType.REQUEST.value

            return self.queryset.filter(
                project = self.kwargs['project_id']
            )

        else:

            raise ValueError('Unknown ticket type. kwarg `ticket_type` must be set')

        return self.queryset.filter(
            ticket_type = ticket_type
        )
