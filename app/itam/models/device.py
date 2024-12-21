import json
import re

from datetime import timedelta

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.reverse import reverse

from access.fields import *
from access.models import TenancyObject

from app.helpers.merge_software import merge_software

from core.classes.icon import Icon
from core.mixin.history_save import SaveHistory
from core.signal.ticket_linked_item_delete import TicketLinkedItem, deleted_model

from itam.models.device_common import DeviceCommonFields, DeviceCommonFieldsName
from itam.models.device_models import DeviceModel
from itam.models.software import Software, SoftwareVersion
from itam.models.operating_system import OperatingSystemVersion

from settings.models.app_settings import AppSettings



class DeviceType(DeviceCommonFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Device Type'

        verbose_name_plural = 'Device Types'


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                }
            ]
        },
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'name',
        'organization',
        'created',
        'modified'
    ]


    def clean(self):

        app_settings = AppSettings.objects.get(owner_organization=None)

        if app_settings.device_type_is_global:

            self.organization = app_settings.global_organization
            self.is_global = app_settings.device_type_is_global


    def __str__(self):

        return self.name



class Device(DeviceCommonFieldsName, SaveHistory):


    class Meta:

        ordering = [
            'name',
            'organization'
        ]

        verbose_name = 'Device'

        verbose_name_plural = 'Devices'


    reserved_config_keys: list = [
        'software'
    ]

    def validate_config_keys_not_reserved(self):

        if self:

            value: dict = self

            for invalid_key in Device.reserved_config_keys:

                if invalid_key in value.keys():
                    raise ValidationError(f'json key "{invalid_key}" is a reserved configuration key')


    def validate_uuid_format(self):

        pattern = r'[0-9|a-f|A-F]{8}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{12}'

        if not re.match(pattern, str(self)):

            raise serializers.ValidationError(
                f'UUID must be formated to match regex {str(pattern)}',
                code = 'invalid_uuid'
            )


    def validate_hostname_format(self):

        pattern = r'^[a-z]{1}[a-z|0-9|\-]+[a-z|0-9]{1}$'

        if not re.match(pattern, str(self).lower()):

            raise serializers.ValidationError(
                '''[RFC1035 2.3.1] A hostname must start with a letter, end with a letter or digit,
                and have as interior characters only letters, digits, and hyphen.''',
                code = 'invalid_hostname'
            )


    name = models.CharField(
        blank = False,
        help_text = 'Hostname of this device',
        max_length = 50,
        unique = True,
        validators = [ validate_hostname_format ],
        verbose_name = 'Name'
    )

    serial_number = models.CharField(
        blank = True,
        default = None,
        help_text = 'Serial number of the device.',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'Serial Number',
        
    )

    uuid = models.CharField(
        blank = True,
        default = None,
        help_text = 'System GUID/UUID.',
        max_length = 50,
        null = True,
        unique = True,
        validators = [ validate_uuid_format ],
        verbose_name = 'UUID'
    )

    device_model = models.ForeignKey(
        DeviceModel,
        blank= True,
        default = None,
        help_text = 'Model of the device.',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Model'
    )

    device_type = models.ForeignKey(
        DeviceType,
        blank= True,
        default = None,
        help_text = 'Type of device.',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Type'
    )


    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Configuration for this device',
        null = True,
        validators=[ validate_config_keys_not_reserved ],
        verbose_name = 'Host Configuration',
    )

    inventorydate = models.DateTimeField(
        blank = True,
        help_text = 'Date and time of the last inventory',
        null = True,
        verbose_name = 'Last Inventory Date',
    )

    is_virtual = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is this device a virtual machine',
        null = False,
        verbose_name = 'Is Virtual',
    )

    table_fields: list = [
        'status_icon',
        "name",
        "device_model",
        "device_type",
        "organization",
        "created",
        "modified",
        "model",
        "nbsp"
    ]

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'device_type',
                        'device_model',
                        'name',
                        'serial_number',
                        'uuid',
                        'inventorydate',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                        'is_virtual',
                        'is_global',
                    ]
                },
                {
                    "layout": "table",
                    "name": "Operating System",
                    "field": "operating_system",
                },
                {
                    "layout": "table",
                    "name": "Dependent Services",
                    "field": "service",
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
                }
            ]
        },
        {
            "name": "Software",
            "slug": "software",
            "sections": [
                {
                    "layout": "table",
                    "field": "software",
                }
            ]
        },
        {
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
                }
            ],
        },
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
        {
            "name": "Config Management",
            "slug": "config_management",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        "rendered_config",
                    ]
                }
            ]
        }
    ]


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ):
        """ Save Device Model

        After saving the device update the related items so that they are a part
        of the same organization as the device.
        """

        if self.uuid is not None:

            self.uuid = str(self.uuid).lower()


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
    def status_icon(self) -> list([Icon]):

        icons: list(Icon) = []

        icons += [
            Icon(
                name = f'device_status_{self.status.lower()}',
                style = f'icon-device-status-{self.status.lower()}'
            )
        ]

        return icons


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

        status: str = 'UNK'

        if (now() - check_date).days >= 0 and (now() - check_date).days <= 1:

            status = 'OK'

        elif (now() - check_date).days >= 2 and (now() - check_date).days < 3:

            status = 'WARN'

        elif (now() - check_date).days >= 3:

            status = 'BAD'

        return status


    @property
    def get_configuration(self):

        softwares = DeviceSoftware.objects.filter(device=self.id)

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



@receiver(post_delete, sender=Device, dispatch_uid='device_delete_signal')
def signal_deleted_model(sender, instance, using, **kwargs):

    deleted_model.send(sender='device_deleted', item_id=instance.id, item_type = TicketLinkedItem.Modules.DEVICE)




class DeviceSoftware(DeviceCommonFields, SaveHistory):
    """ A way for the device owner to configure software to install/remove """

    class Meta:
        ordering = [
            '-action',
            'software'
        ]

        verbose_name = 'Device Software'

        verbose_name_plural = 'Device Softwares'



    class Actions(models.IntegerChoices):
        INSTALL = 1, 'Install'
        REMOVE = 0, 'Remove'


    device = models.ForeignKey(
        Device,
        blank= False,
        help_text = 'Device this software is on',
        on_delete=models.CASCADE,
        null = False,
        verbose_name = 'Device'
    )

    software = models.ForeignKey(
        Software,
        blank= False,
        help_text = 'Software Name',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'Software'
    )

    action = models.IntegerField(
        blank = True,
        choices=Actions,
        default=None,
        help_text = 'Action to perform',
        null=True,
        verbose_name = 'Action',
    )

    version = models.ForeignKey(
        SoftwareVersion,
        blank= True,
        default = None,
        help_text = 'Version to install',
        on_delete=models.CASCADE,
        null = True,
        verbose_name = 'Desired Version'
    )


    installedversion = models.ForeignKey(
        SoftwareVersion,
        blank= True,
        default = None,
        help_text = 'Version that is installed',
        null = True,
        on_delete=models.CASCADE,
        related_name = 'installedversion',
        verbose_name = 'Installed Version'
    )

    installed = models.DateTimeField(
        blank = True,
        help_text = 'Date detected as installed',
        null = True,
        verbose_name = 'Date Installed'
    )


    page_layout: list = []


    table_fields: list = [
        "nbsp",
        "software",
        "category",
        "action_badge",
        "version",
        "installedversion",
        "installed",
        "nbsp"
    ]


    @property
    def action_badge(self):

        from core.classes.badge import Badge

        text:str = 'Add'

        if self.action:

            text = self.get_action_display()

        return Badge(
            icon_name = f'action_{text.lower()}',
            icon_style = f'badge-icon-action-{text.lower()}',
            text = text,
            text_style = f'badge-text-action-{text.lower()}',
            url = '_self',
        )


    def get_url_kwargs(self) -> dict:

        return {
            'device_id': self.device.id,
            'pk': self.id
        }


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

        ordering = [
            'device',
        ]

        verbose_name = 'Device Operating System'

        verbose_name_plural = 'Device Operating Systems'


    device = models.OneToOneField(
        Device,
        blank = False,
        help_text = 'Device for the Operating System',
        on_delete = models.CASCADE,
        null = False,
        verbose_name = 'Device',
        unique = True
    )

    operating_system_version = models.ForeignKey(
        OperatingSystemVersion,
        blank = False,
        help_text = 'Operating system version',
        null = False,
        on_delete = models.CASCADE,
        verbose_name = 'Operating System/Version',
        
    )

    version = models.CharField(
        blank = False,
        help_text = 'Version detected as installed',
        max_length = 15,
        null = False,
        verbose_name = 'Installed Version',
    )

    installdate = models.DateTimeField(
        blank = True,
        default = None,
        help_text = 'Date and time detected as installed',
        null = True,
        verbose_name = 'Install Date',
    )

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        'operating_system_version',
                        'version',
                        'installdate'
                    ],
                }
            ]
        }
    ]

    table_fields: list = [
        'device',
        'operating_system_version',
        'version',
        'installdate',
    ]


    def get_url_kwargs(self) -> dict:

        return {
            'device_id': self.device.id,
            'pk': self.pk
        }


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
