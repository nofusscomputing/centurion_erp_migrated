from django import forms
from django.db.models import Q
from django.forms import ValidationError

from app import settings

from core.forms.common import CommonModelForm

from core.models.ticket.ticket_linked_items import TicketLinkedItem


class TicketLinkedItemForm(CommonModelForm):

    prefix = 'ticket_linked_item'

    class Meta:
        model = TicketLinkedItem
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['organization'].widget = self.fields['organization'].hidden_widget()
        self.fields['ticket'].widget = self.fields['ticket'].hidden_widget()
