from django.urls import reverse

from rest_framework import serializers

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

        if item.ticket_type == self.Meta.model.TicketType.CHANGE.value:

            view_name = '_api_itim_change'
        
        elif item.ticket_type == self.Meta.model.TicketType.INCIDENT.value:

            view_name = '_api_itim_incident'

        elif item.ticket_type == self.Meta.model.TicketType.PROBLEM.value:

            view_name = '_api_itim_problem'

        elif item.ticket_type == self.Meta.model.TicketType.REQUEST.value:

            view_name = '_api_assistance_request'

        else:

            raise ValueError('Serializer unable to obtain ticket type')


        return request.build_absolute_uri(
            reverse(
                'API:' + view_name + '-detail',
                kwargs={
                    'ticket_type': self._kwargs['context']['view'].kwargs['ticket_type'],
                    'pk': item.id
                }
            )
        )


    ticket_comments = serializers.SerializerMethodField('get_url_ticket_comments')


    def get_url_ticket_comments(self, item):

        request = self.context.get('request')

        if item.ticket_type == self.Meta.model.TicketType.CHANGE.value:

            view_name = '_api_itim_change_ticket_comments'
        
        elif item.ticket_type == self.Meta.model.TicketType.INCIDENT.value:

            view_name = '_api_itim_incident_ticket_comments'

        elif item.ticket_type == self.Meta.model.TicketType.PROBLEM.value:

            view_name = '_api_itim_problem_ticket_comments'

        elif item.ticket_type == self.Meta.model.TicketType.REQUEST.value:

            view_name = '_api_assistance_request_ticket_comments'

        else:

            raise ValueError('Serializer unable to obtain ticket type')


        return request.build_absolute_uri(
            reverse(
                'API:' + view_name + '-list',
                kwargs={
                    'ticket_type': self._kwargs['context']['view'].kwargs['ticket_type'],
                    'ticket_id': item.id
                }
            )
        )


    class Meta:
        model = Ticket
        fields =  [
            'id',
            'assigned_teams',
            'assigned_users',
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


    def is_valid(self, *, raise_exception=True) -> bool:

        self.request = self._context['request']

        is_valid = super().is_valid(raise_exception=raise_exception)

        if self.instance:

            ticket_type_choice_id = int(self.instance.ticket_type)
            self.original_object = self.Meta.model.objects.get(pk=self.instance.pk)

        else:

            ticket_type_choice_id = int(self.initial_data['ticket_type'])
            self.original_object = None

        self._ticket_type = str(self.fields['ticket_type'].choices[ticket_type_choice_id]).lower().replace(' ', '_')


        is_valid = self.validate_ticket()

        return is_valid
