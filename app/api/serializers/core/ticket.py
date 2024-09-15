from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from api.serializers.core.ticket_comment import TicketCommentSerializer

from core.forms.validate_ticket import TicketValidation
from core.models.ticket.ticket import Ticket



class TicketSerializer(
    serializers.ModelSerializer,
    TicketValidation,
):

    url = serializers.SerializerMethodField('get_url_ticket')


    def get_url_ticket(self, item):

        request = self.context.get('request')

        kwargs: dict = {
            'pk': item.id
        }

        if item.ticket_type == self.Meta.model.TicketType.CHANGE.value:

            view_name = '_api_itim_change'
        
        elif item.ticket_type == self.Meta.model.TicketType.INCIDENT.value:

            view_name = '_api_itim_incident'

        elif item.ticket_type == self.Meta.model.TicketType.PROBLEM.value:

            view_name = '_api_itim_problem'

        elif item.ticket_type == self.Meta.model.TicketType.REQUEST.value:

            view_name = '_api_assistance_request'

        elif item.ticket_type == self.Meta.model.TicketType.PROJECT_TASK.value:

            view_name = '_api_project_tasks'

            kwargs.update({'project_id': item.project.id})
        else:

            raise ValueError('Serializer unable to obtain ticket type')


        return request.build_absolute_uri(
            reverse(
                'API:' + view_name + '-detail',
                kwargs = kwargs
            )
        )


    ticket_comments = serializers.SerializerMethodField('get_url_ticket_comments')


    def get_url_ticket_comments(self, item):

        request = self.context.get('request')

        kwargs: dict = {
            'ticket_id': item.id
        }

        if item.ticket_type == self.Meta.model.TicketType.CHANGE.value:

            view_name = '_api_itim_change_ticket_comments'
        
        elif item.ticket_type == self.Meta.model.TicketType.INCIDENT.value:

            view_name = '_api_itim_incident_ticket_comments'

        elif item.ticket_type == self.Meta.model.TicketType.PROBLEM.value:

            view_name = '_api_itim_problem_ticket_comments'

        elif item.ticket_type == self.Meta.model.TicketType.REQUEST.value:

            view_name = '_api_assistance_request_ticket_comments'

        elif item.ticket_type == self.Meta.model.TicketType.PROJECT_TASK.value:

            view_name = '_api_project_tasks_comments'

            kwargs.update({'project_id': item.project.id})

        else:

            raise ValueError('Serializer unable to obtain ticket type')


        return request.build_absolute_uri(
            reverse(
                'API:' + view_name + '-list',
                kwargs = kwargs
            )
        )


    class Meta:

        model = Ticket


        fields =  [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'title',
            'description',
            'urgency',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'opened_by',
            'organization',
            'project',
            'subscribed_teams',
            'subscribed_users',
            'ticket_comments',
            'url',
        ]

        read_only_fields = [
            'id',
            'url',
        ]

    
    def __init__(self, instance=None, data=empty, **kwargs):

        self.fields.fields['status'].initial = Ticket.TicketStatus.All.NEW
        self.fields.fields['status'].default = Ticket.TicketStatus.All.NEW

        self.ticket_type_fields = self.Meta.fields

        super().__init__(instance=instance, data=data, **kwargs)

        self.fields['organization'].required = True


    def is_valid(self, *, raise_exception=True) -> bool:

        self.request = self._context['request']

        is_valid = super().is_valid(raise_exception=raise_exception)

        self._ticket_type = str(self.fields['ticket_type'].choices[self._context['view']._ticket_type_value]).lower().replace(' ', '_')


        is_valid = self.validate_ticket()

        self.validated_data['ticket_type'] = int(self._context['view']._ticket_type_value)

        if self.instance is None:

            self.validated_data['subscribed_users'] = self.validated_data['subscribed_users'] + [ self.validated_data['opened_by'] ]

        return is_valid
