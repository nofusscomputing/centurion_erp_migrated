from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty


from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentCategorySerializer(
    serializers.ModelSerializer,
):

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_ticket_comment_category-detail", format="html"
    )


    class Meta:

        model = TicketCommentCategory

        fields = '__all__'

        read_only_fields = [
            'id',
            'url',
        ]


    def __init__(self, instance=None, data=empty, **kwargs):

        if instance is not None:

            if hasattr(instance, 'id'):

                self.fields.fields['parent'].queryset = self.fields.fields['parent'].queryset.exclude(
                    id=instance.id
                )

        super().__init__(instance=instance, data=data, **kwargs)
