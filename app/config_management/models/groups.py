from django.db import models

from access.fields import *
from access.models import TenancyObject

from core.mixin.history_save import SaveHistory



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

    def __str__(self):

        return self.name



class ConfigGroups(GroupsCommonFields, SaveHistory):


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



    def save(self, *args, **kwargs):

        self.is_global = False

        if self.parent:
            self.organization = ConfigGroups.objects.get(id=self.parent.id).organization

        super().save(*args, **kwargs)


