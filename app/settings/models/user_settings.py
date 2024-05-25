from django.contrib.auth.models import User
from django.db import models

from access.fields import *
from access.models import Organization


class UserSettingsCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    slug = None

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class UserSettings(UserSettingsCommonFields):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank= False,
    )


    default_organization = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        blank= True,
        default = None,
        null = True,
    )

    def is_owner(self, user: int) -> bool:

        if user == self.user:

            return True

        return False
