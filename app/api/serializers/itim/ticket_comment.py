from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from core.models.ticket.ticket_comment import Ticket, TicketComment



class TicketCommentSerializer(serializers.ModelSerializer):


    url = serializers.SerializerMethodField('get_url_ticket_comment')

    def get_url_ticket_comment(self, item):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_core_ticket_comments-detail', args=[item.ticket_id, item.pk]))


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
        
        super().__init__(instance=instance, data=data, **kwargs)
