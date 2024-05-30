from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group, Permission

from .fields import *

from core.middleware.get_request import get_request
from core.mixin.history_save import SaveHistory


class Organization(SaveHistory):

    class Meta:
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.slug == '_':
            self.slug = self.name.lower().replace(' ', '_')

        super().save(*args, **kwargs)

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def get_organization(self):
        return self


class TenancyObject(models.Model):

    class Meta:
        abstract = True

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank = False,
        null = True,
    )

    is_global = models.BooleanField(
        default = False,
        blank = False
    )

    def get_organization(self) -> Organization:
        return self.organization


class Team(Group, TenancyObject, SaveHistory):
    class Meta:
        # proxy = True
        verbose_name_plural = "Teams"
        ordering = ['team_name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.name = self.organization.name.lower().replace(' ', '_') + '_' + self.team_name.lower().replace(' ', '_')

        super().save(*args, **kwargs)


    team_name = models.CharField(
        verbose_name = 'Name',
        blank = False,
        max_length = 50,
        unique = False,
        default = ''
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def permission_list(self) -> list:

        permission_list = []

        for permission in self.permissions.all():

            if str(permission.content_type.app_label + '.' + permission.codename) in permission_list:
                continue

            permission_list += [ str(permission.content_type.app_label + '.' + permission.codename) ]

        return [permission_list, self.permissions.all()]



class TeamUsers(SaveHistory):

    class Meta:
        # proxy = True
        verbose_name_plural = "Team Users"
        ordering = ['user']

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    team = models.ForeignKey(
        Team,
        related_name="team",
        on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    manager = models.BooleanField(
        verbose_name='manager',
        default=False,
        blank=True
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def delete(self, using=None, keep_parents=False):
        """ Delete Team

        Overrides, post-action
            As teams are an extension of Groups, remove the user to the team.
        """

        super().delete(using=using, keep_parents=keep_parents)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)
        
        user.groups.remove(group)


    def get_organization(self) -> Organization:
        return self.team.organization


    def save(self, *args, **kwargs):
        """ Save Team

        Overrides, post-action
            As teams are an extension of groups, add the user to the matching group.
        """

        super().save(*args, **kwargs)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)

        user.groups.add(group) 

