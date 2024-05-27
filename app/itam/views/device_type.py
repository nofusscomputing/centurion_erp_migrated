from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from ..models.device import DeviceType

from settings.models.user_settings import UserSettings



class View(OrganizationPermission, generic.UpdateView):
    model = DeviceType
    permission_required = [
        'itam.view_device_type'
    ]
    template_name = 'form.html.j2'

    fields = [
        "name",
        'slug',
        'id',
        'organization',
        'is_global',
    ]

    context_object_name = "device_category"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_delete_url'] = reverse('Settings:_device_type_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_type_view', args=(self.kwargs['pk'],))



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = DeviceType
    permission_required = [
        'access.add_device_type',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'organization',
        'is_global'
    ]


    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_types')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device Type'

        return context

class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = DeviceType
    permission_required = [
        'access.delete_device_type',
    ]
    template_name = 'form.html.j2'
    # fields = [
    #     'name',
    #     'organization',
    #     'is_global'
    # ]


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_types')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
