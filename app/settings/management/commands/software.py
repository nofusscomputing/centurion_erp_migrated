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
            for software in Software.objects.filter(is_global = False):

                software.clean()
                software.save()
            
                self.stdout.write(f"Setting {software} as global")

        if kwargs['migrate']:

            app_settings = AppSettings.objects.get(owner_organization=None)

            for software in Software.objects.filter(
                ~Q(organization = app_settings.global_organization)
                |
                Q(is_global = False),
                Q(organization=app_settings.global_organization),
            ):

                software.clean()
                software.save()
            
                self.stdout.write(f"Migrating {software} to organization {app_settings.global_organization.name}")
