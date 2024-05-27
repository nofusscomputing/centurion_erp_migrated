from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from ..models.software import Software, SoftwareCategory

from settings.models.user_settings import UserSettings


class View(OrganizationPermission, generic.UpdateView):
    model = SoftwareCategory
    permission_required = [
        'itam.view_software'
    ]
    template_name = 'form.html.j2'

    fields = [
        "name",
        'slug',
        'id',
        'organization',
        'is_global',
    ]

    context_object_name = "software"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_delete_url'] = reverse('Settings:_software_category_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_software_category_view', args=(self.kwargs['pk'],))



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = SoftwareCategory
    permission_required = [
        'access.add_software',
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

        return reverse('Settings:_software_categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software Category'

        return context

class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = SoftwareCategory
    permission_required = [
        'access.delete_software',
    ]
    template_name = 'form.html.j2'
    # fields = [
    #     'name',
    #     'organization',
    #     'is_global'
    # ]


    def get_success_url(self, **kwargs):

        return reverse('Settings:_software_categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
