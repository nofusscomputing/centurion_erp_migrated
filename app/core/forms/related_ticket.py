from django import forms
from django.db.models import Q

from app import settings

from core.forms.common import CommonModelForm

from core.models.ticket.ticket import RelatedTickets


class RelatedTicketForm(CommonModelForm):

    prefix = 'ticket'

    class Meta:
        model = RelatedTickets
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['from_ticket_id'].widget = self.fields['from_ticket_id'].hidden_widget()


    def clean(self):
        
        cleaned_data = super().clean()

        return cleaned_data

    def is_valid(self) -> bool:

        is_valid = super().is_valid()

        return is_valid
