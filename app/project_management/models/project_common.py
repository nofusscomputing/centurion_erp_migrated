from django.db import models

from access.fields import *
from access.models import TenancyObject


class ProjectCommonFields(TenancyObject):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this Item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()



class ProjectCommonFieldsName(ProjectCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        help_text = 'Name of the item',
        max_length = 100,
        unique = True,
        verbose_name = 'Name'
    )

    slug = AutoSlugField()
