from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory


from itam.models.device_common import DeviceCommonFields, DeviceCommonFieldsName
from itam.models.device_models import DeviceModel
from itam.models.software import Software, SoftwareVersion
from itam.models.operating_system import OperatingSystemVersion

from settings.models.app_settings import AppSettings

class DeviceType(DeviceCommonFieldsName):


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_type_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.device_type_is_global


    def __str__(self):

        return self.name



class Device(DeviceCommonFieldsName, SaveHistory):

    serial_number = models.CharField(
        verbose_name = 'Serial Number',
        max_length = 50,
        default = None,
        null = True,
        blank = True,
        unique = True,
        
    )

    uuid = models.CharField(
        verbose_name = 'UUID',
        max_length = 50,
        default = None,
        null = True,
        blank = True,
        unique = True,
        
    )

    device_model = models.ForeignKey(
        DeviceModel,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
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


class DeviceSoftware(DeviceCommonFields, SaveHistory):
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



class DeviceOperatingSystem(DeviceCommonFields, SaveHistory):

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
