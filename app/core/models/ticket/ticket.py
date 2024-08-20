from django.db import models

from access.models import TenancyObject



class TicketCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Ticket ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Ticket(
    TenancyObject,
    TicketCommonFields,
):


    class Meta:

        ordering = [
            'id'
        ]

