from django.db import models

from access.fields import *
from access.models import TenancyObject


class DeviceCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class DeviceCommonFieldsName(DeviceCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        help_text = 'The items name',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    slug = AutoSlugField()
