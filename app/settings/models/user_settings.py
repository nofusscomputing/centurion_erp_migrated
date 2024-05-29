from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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


    @receiver(post_save, sender=User)
    def new_user_callback(sender, **kwargs):
        settings = UserSettings.objects.filter(user=kwargs['instance'])

        if not settings.exists():

            UserSettings.objects.create(user=kwargs['instance'])

            # settings = UserSettings.objects.filter(user=context.user)


    def is_owner(self, user: int) -> bool:

        if user == self.user:

            return True

        return False
