from django.contrib.auth import decorators as auth_decorator
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic


from access.mixin import OrganizationPermission
from core.models.manufacturer import Manufacturer



class Index(OrganizationPermission, generic.ListView):

    context_object_name = "list"

    model = Manufacturer

    paginate_by = 10

    permission_required = [
        'core.view_devicetype'
    ]

    template_name = 'settings/manufacturers.html.j2'


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.model.objects.filter().order_by('name')

        else:

            return self.model.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Manufacturers'

        return context




class View(OrganizationPermission, generic.UpdateView):

    context_object_name = "manufacturer"

    fields = [
        "name",
        'slug',
        'id',
        'organization',
        'is_global',
        'model_notes',
    ]

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



class Add(OrganizationPermission, generic.CreateView):

    fields = [
        'name',
        'organization',
        'is_global'
    ]

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


class Delete(OrganizationPermission, generic.DeleteView):

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

