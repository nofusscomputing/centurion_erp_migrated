from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from itam.models.device_models import DeviceModel

from settings.models.app_settings import AppSettings



class Command(BaseCommand):
    help = 'Manage ITAM Device Models for the entire application.'


    def add_arguments(self, parser):
        parser.add_argument('-g', '--global', action='store_true', help='Sets all device models to be global (device models will be migrated to global organization if set)')
        parser.add_argument('-m', '--migrate', action='store_true', help='Migrate existing global device models to global organization')


    def handle(self, *args, **kwargs):
        
        if kwargs['global']:

            softwares = DeviceModel.objects.filter(is_global = False)

            self.stdout.write('Running global')

            self.stdout.write(f'found device model {str(len(softwares))} to set as global')

            for software in softwares:

                software.clean()
                software.save()
            
                self.stdout.write(f"Setting {software} as global")

            self.stdout.write('Global finished')


        if kwargs['migrate']:

            app_settings = AppSettings.objects.get(owner_organization=None)

            self.stdout.write('Running Migrate')
            self.stdout.write(f'Global organization: {app_settings.global_organization}')

            softwares = DeviceModel.objects.filter(
                ~Q(organization = app_settings.global_organization)
                |
                Q(is_global = False)
                &
                Q(organization=app_settings.global_organization),
            )

            self.stdout.write(f'found device model {str(len(softwares))} to migrate')

            for software in softwares:

                software.clean()
                software.save()

                self.stdout.write(f"Migrating model {software} to organization {app_settings.global_organization.name}")

            self.stdout.write('Migrate finished')
