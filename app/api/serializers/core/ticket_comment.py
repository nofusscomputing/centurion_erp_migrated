from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from core.models.ticket.ticket_comment import Ticket, TicketComment



class TicketCommentSerializer(serializers.ModelSerializer):


    url = serializers.SerializerMethodField('get_url_ticket_comment')

    def get_url_ticket_comment(self, item):

        request = self.context.get('request')

        if item.ticket.ticket_type == item.ticket.__class__.TicketType.CHANGE:

            view_name = '_api_itim_change_ticket_comments'
        
        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.INCIDENT:

            view_name = '_api_itim_incident_ticket_comments'

        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.PROBLEM:

            view_name = '_api_itim_problem_ticket_comments'

        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.REQUEST:

            view_name = '_api_assistance_request_ticket_comments'

        else:

            raise ValueError('Serializer unable to obtain ticket type')


        return request.build_absolute_uri(
            reverse('v1:' + view_name + '-detail',
                kwargs={
                    'ticket_id': item.ticket.id,
                    'pk': item.id
                }
            )
        )



    class Meta:
        model = TicketComment
        
        fields = '__all__'

    
    def __init__(self, instance=None, data=empty, **kwargs):

        if 'context' in self._kwargs:

            if 'view' in self._kwargs['context']:

                if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                    ticket = Ticket.objects.get(pk=int(self._kwargs['context']['view'].kwargs['ticket_id']))
                    self.fields.fields['organization'].initial = ticket.organization.id

                    self.fields.fields['ticket'].initial = int(self._kwargs['context']['view'].kwargs['ticket_id'])

                    self.fields.fields['comment_type'].initial = TicketComment.CommentType.COMMENT

                    self.fields.fields['user'].initial = kwargs['context']['request']._user.id

        super().__init__(instance=instance, data=data, **kwargs)
