from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic

from access.mixin import OrganizationPermission

from ..models.software import Software, SoftwareCategory

from settings.models.user_settings import UserSettings



class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    model = Software
    permission_required = 'itam.view_software'
    template_name = 'itam/software_index.html.j2'
    context_object_name = "softwares"


    def get_queryset(self):

        if self.request.user.is_superuser:

            return Software.objects.filter().order_by('name')

        else:

            return Software.objects.filter(organization=self.user_organizations()).order_by('name')



class View(OrganizationPermission, generic.UpdateView):
    model = Software
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

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return f"/settings/software_category/{self.kwargs['pk']}/"



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

        return f"/settings/software_category"


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

        return f"/settings/software_category"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
