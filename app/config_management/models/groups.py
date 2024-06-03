import json

from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory

from itam.models.device import Device



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


    def validate_config_keys(self):

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
        validators=[validate_config_keys]
    )



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



    def render_config(self) -> str:

        config: dict = dict()

        if self.parent:

            config.update(json.loads(ConfigGroups.objects.get(id=self.parent.id).render_config()))

        if self.config:

            config.update(self.config)

        return json.dumps(config)



    def save(self, *args, **kwargs):

        self.is_global = False

        if self.parent:
            self.organization = ConfigGroups.objects.get(id=self.parent.id).organization

        super().save(*args, **kwargs)

    def __str__(self):

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
