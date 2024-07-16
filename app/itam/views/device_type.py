from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itam.models.device import DeviceType
from itam.forms.device_type import DeviceTypeForm




class View(ChangeView):

    form_class = DeviceTypeForm

    model = DeviceType

    permission_required = [
        'itam.view_devicetype',
        'itam.change_devicetype'
    ]

    template_name = 'form.html.j2'

    context_object_name = "device_category"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_delete_url'] = reverse('Settings:_device_type_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_type_view', args=(self.kwargs['pk'],))


    @method_decorator(auth_decorator.permission_required("itam.change_devicetype", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(AddView):

    form_class = DeviceTypeForm

    model = DeviceType

    permission_required = [
        'itam.add_devicetype',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Settings:_device_types')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Device Type'

        return context



class Delete(DeleteView):
    model = DeviceType
    permission_required = [
        'itam.delete_devicetype',
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
