from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory



class OperatingSystemCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class OperatingSystemFieldsName(OperatingSystemCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()



class OperatingSystem(OperatingSystemFieldsName, SaveHistory):

    def __str__(self):

        return self.name


class OperatingSystemVersion(OperatingSystemCommonFields, SaveHistory):

    operating_system = models.ForeignKey(
        OperatingSystem,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name = 'Major Version',
        blank = False,
        max_length = 50,
        unique = False,
    )

    def __str__(self):

        return self.operating_system.name + ' ' + self.name

