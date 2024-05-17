from django.db import models

from access.fields import *
from access.models import TenancyObject
from itam.models.software import Software



class DeviceCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class DeviceCommonFieldsName(DeviceCommonFields):

    class Meta:
        abstract = True

    name = models.CharField(
        blank = False,
        max_length = 50,
        unique = True,
    )

    slug = AutoSlugField()



class DeviceType(DeviceCommonFieldsName):

    def __str__(self):

        return self.name



class Device(DeviceCommonFieldsName):

    serial_number = models.CharField(
        verbose_name = 'Serial Number',
        max_length = 50,
        default = None,
        null = True,
        blank = True
        
    )

    uuid = models.CharField(
        verbose_name = 'UUID',
        max_length = 50,
        default = None,
        null = True,
        blank = True
        
    )


    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.CASCADE,
        default = None,
        null = True,
        blank= True
        
    )

    def __str__(self):

        return self.name

    def get_configuration(self, id):

        softwares = DeviceSoftware.objects.filter(device=id)

        config = {
            "software": []
        }

        for software in softwares:
            
            if int(software.action) == 1:

                state = 'present'

            elif int(software.action) == 0:

                state = 'absent'

            software = {
                "name": software.software.slug,
                "state": state
            }
            config['software'] = config['software'] + [ software ]

        return config



class DeviceSoftware(DeviceCommonFields):
    """ A way for the device owner to configure software to install/remove """


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
    )
