from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic


from access.mixin import OrganizationPermission

from core.forms.manufacturer import ManufacturerForm
from core.models.manufacturer import Manufacturer
from core.views.common import AddView, ChangeView, DeleteView, IndexView



class Index(IndexView):

    context_object_name = "list"

    model = Manufacturer

    paginate_by = 10

    permission_required = [
        'core.view_manufacturer'
    ]

    template_name = 'settings/manufacturers.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Manufacturers'

        return context




class View(ChangeView):

    context_object_name = "manufacturer"

    form_class = ManufacturerForm

    model = Manufacturer

    permission_required = [
        'core.view_manufacturer',
        'core.change_manufacturer',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Settings:_manufacturer_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return f"/settings/manufacturer/{self.kwargs['pk']}"


    @method_decorator(auth_decorator.permission_required("core.change_manufacturer", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(AddView):

    
    form_class = ManufacturerForm

    model = Manufacturer

    permission_required = [
        'core.add_manufacturer',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return f"/settings/manufacturers"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Manufacturer'

        return context


class Delete(DeleteView):

    model = Manufacturer

    permission_required = [
        'core.delete_manufacturer',
    ]

    template_name = 'form.html.j2'

    def get_success_url(self, **kwargs):

        return f"/settings/manufacturers"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context

