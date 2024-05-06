from django.contrib import admin
from django.db import models

from organizations.models import Organization, OrganizationUser


class Organization(Organization):
    class Meta:
        proxy = True

    def __str__(self):
        return self.name


class Team(Organization):
    
    organization = models.ForeignKey(Organization, related_name="teams", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Teams"
        ordering = ['name']

    def __str__(self):
        return self.name
