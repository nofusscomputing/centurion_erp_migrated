from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic

from access.mixin import OrganizationPermission

from itam.models.device_models import DeviceModel



class View(OrganizationPermission, generic.UpdateView):
    model = DeviceModel
    permission_required = [
        'itam.view_device_type'
    ]
    template_name = 'form.html.j2'

    fields = [
        "name",
        'slug',
        'manufacturer',
        'id',
        'organization',
        'is_global',
    ]

    context_object_name = "device_model"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return f"/settings/device_model/{self.kwargs['pk']}"



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = DeviceModel
    permission_required = [
        'access.add_device_type',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'manufacturer',
        'organization',
        'is_global'
    ]


    def get_success_url(self, **kwargs):

        return f"/settings/device_models"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device Model'

        return context

class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = DeviceModel
    permission_required = [
        'access.delete_device_type',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return f"/settings/device_models"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
