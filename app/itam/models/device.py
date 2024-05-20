from django.db import models

from access.fields import *
from access.models import TenancyObject
from itam.models.software import Software, SoftwareVersion
from itam.models.operating_system import OperatingSystemVersion


class DeviceCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class DeviceCommonFieldsName(DeviceCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()



class DeviceType(DeviceCommonFieldsName):

    def __str__(self):

        return self.name



class Device(DeviceCommonFieldsName):

    serial_number = models.CharField(
        verbose_name = 'Serial Number',
        max_length = 50,
        default = None,
        null = True,
        blank = True
        
    )

    uuid = models.CharField(
        verbose_name = 'UUID',
        max_length = 50,
        default = None,
        null = True,
        blank = True
        
    )


    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
        
    )


    inventorydate = models.DateTimeField(
        verbose_name = 'Last Inventory Date',
        null = True,
        blank = True
    )


    def __str__(self):

        return self.name


    def get_configuration(self, id):

        softwares = DeviceSoftware.objects.filter(device=id)

        config = {
            "software": []
        }

        for software in softwares:

            if software.action:
            
                if int(software.action) == 1:

                    state = 'present'

                elif int(software.action) == 0:

                    state = 'absent'

                software_action = {
                    "name": software.software.slug,
                    "state": state
                }


                if software.version:
                    software_action['version'] = software.version.name

                config['software'] = config['software'] + [ software_action ]

        return config



class DeviceSoftware(DeviceCommonFields):
    """ A way for the device owner to configure software to install/remove """

    class Meta:
        ordering = [
            '-action',
            'software'
        ]


    class Actions(models.TextChoices):
        INSTALL = '1', 'Install'
        REMOVE = '0', 'Remove'


    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        default = None,
        null = False,
        blank= False
    )

    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
        default = None,
        null = False,
        blank= False
    )

    action = models.CharField(
        max_length=1,
        choices=Actions,
        default=None,
        null=True,
        blank = True,
    )

    version = models.ForeignKey(
        SoftwareVersion,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )


    installedversion = models.ForeignKey(
        SoftwareVersion,
        related_name = 'installedversion',
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )

    installed = models.DateTimeField(
        verbose_name = 'Install Date',
        null = True,
        blank = True
    )



class DeviceOperatingSystem(DeviceCommonFields):

    device = models.ForeignKey(
        Device,
        on_delete = models.CASCADE,
        default = None,
        null = False,
        blank = False,
        
    )

    operating_system_version = models.ForeignKey(
        OperatingSystemVersion,
        verbose_name = 'Operating System/Version',
        on_delete = models.CASCADE,
        default = None,
        null = False,
        blank = False
        
    )

    version = models.CharField(
        verbose_name = 'Installed Version',
        max_length = 15,
        null = False,
        blank = False,
    )

    installdate = models.DateTimeField(
        verbose_name = 'Install Date',
        null = True,
        blank = True,
        default = None,
    )
