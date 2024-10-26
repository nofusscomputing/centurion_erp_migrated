from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from api.serializers.core.ticket_comment import TicketCommentSerializer

from core.forms.validate_ticket import TicketValidation
from core.models.ticket.ticket_category import TicketCategory



class TicketCategorySerializer(
    serializers.ModelSerializer,
):

    url = serializers.HyperlinkedIdentityField(
        view_name="v1:_api_ticket_category-detail", format="html"
    )


    class Meta:

        model = TicketCategory

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
