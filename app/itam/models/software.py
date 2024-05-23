from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory
from core.models.manufacturer import Manufacturer


class SoftwareCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class SoftwareCategory(SoftwareCommonFields, SaveHistory):

    def __str__(self):

        return self.name



class Software(SoftwareCommonFields, SaveHistory):

    publisher = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    category = models.ForeignKey(
        SoftwareCategory,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
        
    )

    def __str__(self):

        return self.name



class SoftwareVersion(SoftwareCommonFields, SaveHistory):

    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = False,
    )

    def __str__(self):

        return self.name



