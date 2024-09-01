from django.urls import reverse

from rest_framework import serializers

from api.serializers.itim.ticket_comment import TicketCommentSerializer

from core.forms.validate_ticket import TicketValidation
from core.models.ticket.ticket import Ticket



class TicketSerializer(
    serializers.ModelSerializer,
    TicketValidation,
):
    
    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_core_tickets-detail", format="html"
    )

    ticket_comments = serializers.SerializerMethodField('get_url_ticket_comments')


    def get_url_ticket_comments(self, item):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_core_ticket_comments-list', args=[item.id]))


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
