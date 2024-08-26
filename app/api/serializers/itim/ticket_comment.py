from django.urls import reverse

from rest_framework import serializers

from core.models.ticket.ticket_comment import TicketComment



class TicketCommentSerializer(serializers.ModelSerializer):


    url = serializers.SerializerMethodField('get_url_ticket_comment')

    def get_url_ticket_comment(self, item):

        request = self.context.get('request')
        return request.build_absolute_uri(reverse('API:_api_core_ticket_comments-detail', args=[item.ticket_id, item.pk]))


    class Meta:
        model = TicketComment
        
        fields = '__all__'
