import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.views import generic

from access.mixin import OrganizationPermission
from access.models import Organization

from ..models.device import Device, DeviceSoftware, DeviceOperatingSystem
from itam.forms.device_softwareadd import SoftwareAdd
from itam.forms.device_softwareupdate import SoftwareUpdate

from itam.forms.device.device import DeviceForm
from itam.forms.device.operating_system import Update as OperatingSystemForm


class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    model = Device
    permission_required = 'itam.view_device'
    template_name = 'itam/device_index.html.j2'
    context_object_name = "devices"

    paginate_by = 10

    def get_queryset(self):

        if self.request.user.is_superuser:

            return Device.objects.filter().order_by('name')

        else:

            return Device.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



def _get_form(request, formcls, prefix, **kwargs):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix, **kwargs)

class View(OrganizationPermission, generic.UpdateView):

    model = Device

    permission_required = [
        'itam.view_device'
    ]

    template_name = 'itam/device.html.j2'

    form_class = DeviceForm

    context_object_name = "device"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        try:
            operating_system_version = DeviceOperatingSystem.objects.get(device=self.kwargs['pk'])
        
        except DeviceOperatingSystem.DoesNotExist:

            operating_system_version = None

        if operating_system_version:

            context['operating_system'] = OperatingSystemForm(prefix='operating_system', instance=operating_system_version)

        else:

            context['operating_system'] = OperatingSystemForm(prefix='operating_system')


        softwares = DeviceSoftware.objects.filter(device=self.kwargs['pk'])
        context['softwares'] = softwares

        config = self.object.get_configuration(self.kwargs['pk'])
        context['config'] = json.dumps(config, indent=4, sort_keys=True)

        context['content_title'] = self.object.name

        return context


    def post(self, request, *args, **kwargs):

        device = Device.objects.get(pk=self.kwargs['pk'])

        try:

            existing_os = DeviceOperatingSystem.objects.get(device=self.kwargs['pk'])

        except DeviceOperatingSystem.DoesNotExist:

            existing_os = None

        operating_system = OperatingSystemForm(request.POST, prefix='operating_system', instance=existing_os)

        if operating_system.is_bound and operating_system.is_valid():

            operating_system.instance.organization = device.organization
            operating_system.instance.device = device

            operating_system.save()

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['pk']}/"



class SoftwareView(OrganizationPermission, generic.UpdateView):
    model = DeviceSoftware
    permission_required = [
        'itam.view_devicesoftware'
    ]
    template_name = 'form.html.j2'



    context_object_name = "devicesoftware"

    form_class = SoftwareUpdate


    def form_valid(self, form):
        device = Device.objects.get(pk=self.kwargs['device_id'])

        form.instance.organization_id = device.organization.id
        form.instance.device_id = self.kwargs['device_id']
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['device_id']}/"



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = Device
    permission_required = [
        'itam.add_device',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'serial_number',
        'uuid',
        'device_type',
        'organization',
    ]

    def form_valid(self, form):
        form.instance.is_global = False
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return f"/itam/device/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device'

        return context



class SoftwareAdd(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = DeviceSoftware
    permission_required = [
        'itam.add_devicesoftware',
    ]
    template_name = 'form.html.j2'
    # fields = [
    #     'software',
    #     'action'
    # ]

    form_class = SoftwareAdd


    def form_valid(self, form):
        device = Device.objects.get(pk=self.kwargs['pk'])
        form.instance.organization_id = device.organization.id
        form.instance.device_id = self.kwargs['pk']
        return super().form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        device = Device.objects.get(pk=self.kwargs['pk'])
        kwargs['organizations'] = [ device.organization.id ]
        return kwargs


    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['pk']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device'

        return context



class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = Device
    permission_required = [
        'itam.delete_device',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return f"/itam/device/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
