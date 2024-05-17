import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.views import generic

from access.mixin import OrganizationPermission
from access.models import Organization

from ..models.device import Device, DeviceSoftware
from itam.forms.device_softwareadd import SoftwareAdd


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



class View(OrganizationPermission, generic.UpdateView):
    model = Device
    permission_required = [
        'itam.view_device'
    ]
    template_name = 'itam/device.html.j2'

    fields = [
        'id',
        'name',
        'serial_number',
        'uuid',
        'device_type',
        'is_global'
    ]

    context_object_name = "device"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        softwares = DeviceSoftware.objects.filter(device=self.kwargs['pk'])

        context['content_title'] = self.object.name
        context['softwares'] = softwares

        config = self.object.get_configuration(self.kwargs['pk'])
        context['config'] = json.dumps(config, indent=4, sort_keys=True)

        return context

    def get_success_url(self, **kwargs):

        return f"/itam/device/{self.kwargs['pk']}/"



class SoftwareView(OrganizationPermission, generic.UpdateView):
    model = DeviceSoftware
    permission_required = [
        'itam.view_devicesoftware'
    ]
    template_name = 'form.html.j2'

    fields = [
        'action',
    ]


    context_object_name = "devicesoftware"


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
        'is_global'
    ]


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
