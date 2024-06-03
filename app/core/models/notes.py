from django.contrib.auth.models import User
from django.db import models

from access.fields import *
from access.models import TenancyObject

from config_management.models.groups import ConfigGroups

from itam.models.device import Device
from itam.models.software import Software
from itam.models.operating_system import OperatingSystem


class NotesCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class Notes(NotesCommonFields):
    """ Notes that can be left against a model 

    Currently supported models are:
        - Device
        - Operating System
        - Software
    """

    class Meta:

        ordering = [
            '-created'
        ]


    note = models.TextField(
        verbose_name = 'Note',
        blank = True,
        default = None,
        null = True
    )


    usercreated = models.ForeignKey(
        User,
        verbose_name = 'Added By',
        related_name = 'usercreated',
        on_delete=models.SET_DEFAULT,
        default = None,
        null = True,
        blank= True
    )

    usermodified = models.ForeignKey(
        User,
        verbose_name = 'Edited By',
        related_name = 'usermodified',
        on_delete=models.SET_DEFAULT,
        default = None,
        null = True,
        blank= True
    )

    config_group = models.ForeignKey(
        ConfigGroups,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    operatingsystem = models.ForeignKey(
        OperatingSystem,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )


    def __str__(self):

        return 'Note ' + str(self.id)
