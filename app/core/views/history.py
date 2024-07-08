import markdown

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic

from access.mixin import OrganizationPermission

from core.models.history import History



class View(OrganizationPermission, generic.View):

    permission_required = [
        'core.view_history'
    ]

    template_name = 'history.html.j2'


    def get_object(self):
        """ Get the history entry model

        function required to check permissions, in particular that the user is in the same organization.

        Raises:
            Exception: if the model can't be found.

        Returns:
            Model: Returns the model Object
        """
        from access.models import Organization, Team

        from itam.models.device import Device, DeviceSoftware, DeviceModel, DeviceType, DeviceOperatingSystem
        from itam.models.operating_system import OperatingSystem
        from itam.models.software import Software, SoftwareCategory

        from core.models.manufacturer import Manufacturer

        from config_management.models.groups import ConfigGroups

        if not hasattr(self, 'model'):

            match self.kwargs['model_name']:

                case 'configgroups':

                    self.model = ConfigGroups

                case 'device':

                    self.model = Device

                case 'devicemodel':

                    self.model = DeviceModel

                case 'devicetype':

                    self.model = DeviceType

                case 'manufacturer':

                    self.model = Manufacturer

                case 'software':

                    self.model = Software

                case 'softwarecategory':

                    self.model = SoftwareCategory

                case 'operatingsystem':

                    self.model = OperatingSystem

                case 'organization':

                    self.model = Organization

                case 'team':

                    self.model = Team

                case _:
                    raise Exception('Unable to determine history items model')

        if not hasattr(self, 'obj'):

            self.obj = self.model.objects.get(id=self.kwargs['model_pk'])

        return self.obj


    def get(self, request, model_name, model_pk):
        if not request.user.is_authenticated and settings.LOGIN_REQUIRED:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        context = {}

        context['history'] = History.objects.filter(
            Q(item_pk = model_pk, item_class = model_name)
            |
            Q(item_parent_pk = model_pk, item_parent_class = model_name)
        )

        context['content_title'] = 'History'

        return render(request, self.template_name, context)
