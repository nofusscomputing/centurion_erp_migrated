from django.contrib.auth.models import User
from django.db import models

from access.fields import *


class HistoryCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID for this history entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()



class History(HistoryCommonFields):


    class Meta:

        ordering = [
            '-created'
        ]

        verbose_name = 'History'

        verbose_name_plural = 'History'


    class Actions(models.TextChoices):
        ADD = '1', 'Create'
        UPDATE = '2', 'Update'
        DELETE = '3', 'Delete'


    before = models.JSONField(
        blank = True,
        default = None,
        help_text = 'JSON Object before Change',
        null = True,
        verbose_name = 'Before'
    )


    after = models.JSONField(
        blank = True,
        default = None,
        help_text = 'JSON Object After Change',
        null = True,
        verbose_name = 'After'
    )


    action = models.IntegerField(
        blank = False,
        choices=Actions,
        default=None,
        help_text = 'History action performed',
        null=True,
        verbose_name = 'Action'
    )


    user = models.ForeignKey(
        User,
        blank= False,
        help_text = 'User whom performed the action this history relates to',
        null = True,
        on_delete=models.DO_NOTHING,
        verbose_name = 'User'
    )

    item_pk = models.IntegerField(
        blank = False,
        default=None,
        help_text = 'Primary Key of the item this history relates to',
        null = True,
        verbose_name = 'Item ID'
    )

    item_class = models.CharField(
        blank = False,
        default=None,
        help_text = 'Class of the item this history relates to',
        null = True,
        max_length = 50,
        unique = False,
    )

    item_parent_pk = models.IntegerField(
        blank = False,
        default=None,
        help_text = 'Primary Key of the Parent Item this history relates to',
        null = True,
        verbose_name = 'Parent ID'
    )

    item_parent_class = models.CharField(
        blank = False,
        default=None,
        help_text = 'Class oof the Paarent Item this history relates to',
        max_length = 50,
        null = True,
        unique = False,
        verbose_name = 'Parent Class'
    )


    table_fields: list  = [
        'created',
        'action',
        'item_class',
        'user',
        'nbsp',
        [
            'before',
            'after'
        ]
    ]
