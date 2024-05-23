from django.contrib.auth.models import User
from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory

class ManufacturerCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Manufacturer(TenancyObject, ManufacturerCommonFields, SaveHistory):


    class Meta:

        ordering = [
            'name'
        ]

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )


    slug = AutoSlugField()


    def __str__(self):

        return self.name
