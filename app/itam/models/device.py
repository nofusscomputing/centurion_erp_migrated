import json
import re

from datetime import timedelta

from django.db import models
from django.forms import ValidationError

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


    class Meta:

        verbose_name_plural = 'Device Types'


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_type_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.device_type_is_global


    def __str__(self):

        return self.name



class Device(DeviceCommonFieldsName, SaveHistory):


    class Meta:

        verbose_name_plural = 'Devices'


    reserved_config_keys: list = [
        'software'
    ]

    def validate_config_keys_not_reserved(self):

        value: dict = self

        for invalid_key in Device.reserved_config_keys:

            if invalid_key in value.keys():
                raise ValidationError(f'json key "{invalid_key}" is a reserved configuration key')


    def validate_uuid_format(self):

        pattern = r'[0-9|a-f]{8}\-[0-9|a-f]{4}\-[0-9|a-f]{4}\-[0-9|a-f]{4}\-[0-9|a-f]{12}'

        if not re.match(pattern, str(self)):

            raise ValidationError(f'UUID Must be in {str(pattern)}')


    def validate_hostname_format(self):

        pattern = r'^[a-z]{1}[a-z|0-9|\-]+[a-z|0-9]{1}$'

        if not re.match(pattern, str(self).lower()):

            raise ValidationError(
                '''[RFC1035 2.3.1] A hostname must start with a letter, end with a letter or digit,
                and have as interior characters only letters, digits, and hyphen.'''
            )


    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
        validators = [ validate_hostname_format ]
    )

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
        validators = [ validate_uuid_format ]
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


    config = models.JSONField(
        blank = True,
        default = None,
        null = True,
        validators=[ validate_config_keys_not_reserved ],
        verbose_name = 'Host Configuration',
        help_text = 'Configuration for this device'
    )

    inventorydate = models.DateTimeField(
        verbose_name = 'Last Inventory Date',
        null = True,
        blank = True,
    )

    is_virtual = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is this device a virtual machine',
        null = False,
        verbose_name = 'Is Virtual',
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

            if self.config:

                config.update(self.config)

            from itim.models.services import Service
            services = Service.objects.filter(
                device = self.pk
            )

            for service in services:

                if service.config_variables:

                    service_config:dict = {
                        service.config_key_variable: service.config_variables
                    }

                    config.update(service_config)

        return config


class DeviceSoftware(DeviceCommonFields, SaveHistory):
    """ A way for the device owner to configure software to install/remove """

    class Meta:
        ordering = [
            '-action',
            'software'
        ]

        verbose_name_plural = 'Device Softwares'



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


    class Meta:

        verbose_name_plural = 'Device Operating Systems'


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
