from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group, Permission

from .fields import *


class Organization(models.Model):

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


class TenancyObject(models.Model):

    class Meta:
        abstract = True

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )

    is_global = models.BooleanField(
        default = False,
        blank = False
    )


class Team(Group, TenancyObject):
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


class TeamUsers(models.Model):

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
