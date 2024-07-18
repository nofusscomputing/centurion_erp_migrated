import json

from datetime import timedelta

from django.db import models

from access.fields import *
from access.models import TenancyObject

from app.helpers.merge_software import merge_software

from core.mixin.history_save import SaveHistory

from itam.models.device_common import DeviceCommonFields, DeviceCommonFieldsName
from itam.models.device_models import DeviceModel
from itam.models.software import Software, SoftwareVersion
from itam.models.operating_system import OperatingSystemVersion

from settings.models.app_settings import AppSettings

class DeviceType(DeviceCommonFieldsName, SaveHistory):


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
        help_text = 'Serial number of the device.',
        
    )

    uuid = models.CharField(
        verbose_name = 'UUID',
        max_length = 50,
        default = None,
        null = True,
        blank = True,
        unique = True,
        help_text = 'System GUID/UUID.',
    )

    device_model = models.ForeignKey(
        DeviceModel,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True,
        help_text = 'Model of the device.',
    )

    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True,
        help_text = 'Type of device.',
    )


    inventorydate = models.DateTimeField(
        verbose_name = 'Last Inventory Date',
        null = True,
        blank = True,
    )

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ):
        """ Save Device Model

        After saving the device update the related items so that they are a part
        of the same organization as the device.
        """

        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        models_to_update =[ 
            DeviceSoftware,
            DeviceOperatingSystem
        ]

        for update_model in models_to_update:

            obj = update_model.objects.filter(
                device = self.id,
            )

            if obj.exists():

                obj.update(
                    is_global = False,
                    organization = self.organization,
                )

        from config_management.models.groups import ConfigGroupHosts

        ConfigGroupHosts.objects.filter(
            host = self.id,
        ).delete()


    def __str__(self):

        return self.name

    @property
    def status(self) -> str:
        """ Fetch Device status

        Returns:
            str: Current status of the item
        """

        if self.inventorydate:

            check_date = self.inventorydate

        else:

            check_date = now() + timedelta(days=99)

        one = (now() - check_date).days

        if (now() - check_date).days >= 0 and (now() - check_date).days <= 1:

            return 'OK'

        elif (now() - check_date).days >= 2 and (now() - check_date).days < 3:

            return 'WARN'

        elif (now() - check_date).days >= 3:

            return 'BAD'

        else:

            return 'UNK'


    def get_configuration(self, id):

        softwares = DeviceSoftware.objects.filter(device=id)

        config = {
            "software": []
        }

        host_software = []
        group_software = []

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

                host_software += [ software_action ]

        config: dict = config

        from config_management.models.groups import ConfigGroupHosts

        if self.id:

            config_groups = ConfigGroupHosts.objects.filter(host=self.id).order_by('group')

            for group in config_groups:

                rendered_config = group.group.render_config()

                if rendered_config:

                    config.update(json.loads(rendered_config))

                    rendered_config: dict = json.loads(rendered_config)

                    if 'software' in rendered_config.keys():
                        
                        group_software = group_software + rendered_config['software']

            config['software'] = merge_software(group_software, host_software)

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


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.device


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ):

        self.is_global = False

        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
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


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.device


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ):

        self.is_global = False

        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
