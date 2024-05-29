from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from itam.models.software import Software

from settings.models.app_settings import AppSettings



class Command(BaseCommand):
    help = 'Manage ITAM Software for the entire application.'


    def add_arguments(self, parser):
        parser.add_argument('-g', '--global', action='store_true', help='Sets all software to be global (software will be migrated to global organization if set)')
        parser.add_argument('-m', '--migrate', action='store_true', help='Migrate existing global software to global organization')


    def handle(self, *args, **kwargs):
        
        if kwargs['global']:

            softwares = Software.objects.filter(is_global = False)

            self.stdout.write('Running global')

            self.stdout.write(f'found {str(len(softwares))} software to set as global')

            for software in softwares:

                software.clean()
                software.save()
            
                self.stdout.write(f"Setting {software} as global")

            self.stdout.write('Global finished')


        if kwargs['migrate']:

            app_settings = AppSettings.objects.get(owner_organization=None)

            self.stdout.write('Running Migrate')
            self.stdout.write(f'Global organization: {app_settings.global_organization}')

            softwares = Software.objects.filter(
                ~Q(organization = app_settings.global_organization)
                |
                Q(is_global = False)
                &
                Q(organization=app_settings.global_organization),
            )

            self.stdout.write(f'found {str(len(softwares))} software to migrate')

            for software in softwares:

                software.clean()
                software.save()

                self.stdout.write(f"Migrating {software} to organization {app_settings.global_organization.name}")

            self.stdout.write('Migrate finished')
