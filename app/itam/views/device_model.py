from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from access.mixin import OrganizationPermission

from itam.models.device_models import DeviceModel

from settings.models.user_settings import UserSettings



class View(OrganizationPermission, generic.UpdateView):
    model = DeviceModel
    permission_required = [
        'itam.view_devicemodel',
        'itam.change_devicemodel',
    ]
    template_name = 'form.html.j2'

    fields = [
        "name",
        'slug',
        'manufacturer',
        'id',
        'organization',
        'is_global',
        'model_notes',
    ]

    context_object_name = "device_model"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Settings:_device_model_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_model_view', args=(self.kwargs['pk'],))


    @method_decorator(auth_decorator.permission_required("itam.change_devicemodel", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(OrganizationPermission, generic.CreateView):
    model = DeviceModel
    permission_required = [
        'itam.add_devicemodel',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'manufacturer',
        'organization',
        'is_global'
    ]


    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_models')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device Model'

        return context



class Delete(OrganizationPermission, generic.DeleteView):
    model = DeviceModel
    permission_required = [
        'itam.delete_devicemodel',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_models')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
