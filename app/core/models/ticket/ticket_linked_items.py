from django.db import models

from .ticket_enum_values import TicketValues

from access.models import TenancyObject

from core.models.ticket.ticket import Ticket



class TicketLinkedItem(TenancyObject):

    class Meta:

        ordering = [
            'id'
        ]

    class Modules(models.TextChoices):
        DEVICE           = 'itam.models.device', 'Device'
        OPERATING_SYSTEM = 'itam.models.operating_system', 'Operating System'
        SOFTWARE         = 'itam.models.software', 'Software'

    is_global = None

    model_notes = None

    id = models.AutoField(
        blank=False,
        help_text = 'ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    ticket = models.ForeignKey(
        Ticket,
        blank= False,
        help_text = 'Ticket the item will be linked to',
        null = False,
        on_delete = models.CASCADE,
        verbose_name = 'Ticket',
    )

    module = models.CharField(
        blank= False,
        choices = Modules,
        help_text = 'Python Model location for linked item',
        null = False,
        verbose_name = 'Item Type',
    )

    item = models.IntegerField(
        blank = False,
        help_text = 'Item ID to link to ticket',
        null = False,
        verbose_name = 'Item ID',
    )
