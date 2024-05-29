from django.contrib.auth.models import User
from django.db import models

from access.fields import *


class HistoryCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()



class History(HistoryCommonFields):


    class Meta:

        ordering = [
            '-created'
        ]


    class Actions(models.TextChoices):
        ADD = '1', 'Create'
        UPDATE = '2', 'Update'
        DELETE = '3', 'Delete'


    before = models.TextField(
        help_text = 'JSON Object before Change',
        blank = True,
        default = None,
        null = True
    )


    after = models.TextField(
        help_text = 'JSON Object After Change',
        blank = True,
        default = None,
        null = True
    )


    action = models.IntegerField(
        choices=Actions,
        default=None,
        null=True,
        blank = False,
    )


    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null = True,
        blank= False,
    )

    item_pk = models.IntegerField(
        default=None,
        null = True,
        blank = False,
    )

    item_class = models.CharField(
        blank = False,
        default=None,
        null = True,
        max_length = 50,
        unique = False,
    )

    item_parent_pk = models.IntegerField(
        default=None,
        null = True,
        blank = False,
    )

    item_parent_class = models.CharField(
        blank = False,
        default=None,
        null = True,
        max_length = 50,
        unique = False,
    )
