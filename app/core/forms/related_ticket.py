from django import forms
from django.db.models import Q
from django.forms import ValidationError

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

        check_db = self.Meta.model.objects.filter(
            to_ticket_id = self.cleaned_data['to_ticket_id'].id,
            from_ticket_id = self.cleaned_data['from_ticket_id'].id,
        )

        check_db_inverse = self.Meta.model.objects.filter(
            to_ticket_id = self.cleaned_data['from_ticket_id'].id,
            from_ticket_id = self.cleaned_data['to_ticket_id'].id,
        )

        if check_db.count() > 0 or check_db_inverse.count() > 0:

            raise ValidationError(f"Ticket is already related to #{self.cleaned_data['to_ticket_id'].id}")

            is_valid = False


        return is_valid
