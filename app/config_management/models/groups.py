import json
import re

from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import TenancyObject

from app.helpers.merge_software import merge_software

from core.mixin.history_save import SaveHistory

from itam.models.device import Device, DeviceSoftware
from itam.models.software import Software, SoftwareVersion



class GroupsCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class ConfigGroups(GroupsCommonFields, SaveHistory):

    reserved_config_keys: list = [
        'software'
    ]


    def validate_config_keys_not_reserved(self):

        value: dict = self

        for invalid_key in ConfigGroups.reserved_config_keys:

            if invalid_key in value.keys():
                raise ValidationError(f'json key "{invalid_key}" is a reserved configuration key')


    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
    )


    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = False,
    )


    config = models.JSONField(
        blank = True,
        default = None,
        null = True,
        validators=[ validate_config_keys_not_reserved ]
    )


    def config_keys_ansible_variable(self, value: dict):

        clean_value = {}

        for key, value in value.items():

            key: str = str(key).lower()
            
            key = re.sub('\s|\.|\-', '_', key) # make an '_' char

            if type(value) is dict:

                clean_value[key] = self.config_keys_ansible_variable(value)

            else:

                clean_value[key] = value

        return clean_value


    def count_children(self) -> int:
        """ Count all child groups recursively

        Returns:
            int: Total count of ALL child-groups
        """

        count = 0

        children = ConfigGroups.objects.filter(parent=self.pk)

        for child in children.all():

            count += 1

            count += child.count_children()

        return count




    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.parent


    def render_config(self) -> str:

        config: dict = dict()

        if self.parent:

            config.update(json.loads(ConfigGroups.objects.get(id=self.parent.id).render_config()))

        if self.config:

            config.update(self.config)

        softwares = ConfigGroupSoftware.objects.filter(config_group=self.id)

        software_actions = {
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

                software_actions['software'] = software_actions['software'] + [ software_action ]

        if len(software_actions['software']) > 0: # don't add empty software as it prevents parent software from being added

            if 'software' not in config.keys():

                config['software'] = []

            config['software'] = merge_software(config['software'], software_actions['software'])

        return json.dumps(config)



    def save(self, *args, **kwargs):

        if self.config:

            self.config = self.config_keys_ansible_variable(self.config)

        if self.parent:
            self.organization = ConfigGroups.objects.get(id=self.parent.id).organization

        if self.pk:

            obj = ConfigGroups.objects.get(
                id = self.id,
            )

            # Prevent organization change. ToDo: add feature so that config can change organizations
            self.organization = obj.organization

        super().save(*args, **kwargs)


    def __str__(self):

        if self.parent:

            return f'{self.parent} > {self.name}'

        return self.name



class ConfigGroupHosts(GroupsCommonFields, SaveHistory):


    def validate_host_no_parent_group(self):
        """ Ensure that the host is not within any parent group

        Raises:
            ValidationError: host exists within group chain
        """

        if False:
            raise ValidationError(f'host {self} is already a member of this chain as it;s a member of group ""')


    host = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        null = False,
        blank= False,
        validators = [ validate_host_no_parent_group ]
    )


    group = models.ForeignKey(
        ConfigGroups,
        on_delete=models.CASCADE,
        null = False,
        blank= False
    )


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.group





class ConfigGroupSoftware(GroupsCommonFields, SaveHistory):
    """ A way to configure software to install/remove per config group """

    class Meta:
        ordering = [
            '-action',
            'software'
        ]


    config_group = models.ForeignKey(
        ConfigGroups,
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
        choices=DeviceSoftware.Actions,
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


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.config_group


