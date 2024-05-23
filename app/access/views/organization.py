from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from access.mixin import *
from access.models import *



class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    permission_required = 'access.view_organization'
    template_name = 'access/index.html.j2'
    context_object_name = "organization_list"


    def get_queryset(self):

        if self.request.user.is_superuser:

            return Organization.objects.filter()

        else:

            return Organization.objects.filter(pk__in=self.user_organizations())



class View(LoginRequiredMixin, OrganizationPermission, generic.UpdateView):
    model = Organization
    permission_required = 'access.view_organization'
    template_name = "access/organization.html.j2"
    fields = ["name", 'id']


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"

    def get_queryset(self):

        return Organization.objects.filter(pk=self.kwargs['pk'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['organization'] = Organization.objects.get(pk=self.kwargs['pk'])

        context['teams'] = Team.objects.filter(organization=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        return context



class Change(LoginRequiredMixin, OrganizationPermission, generic.DetailView):
    pass



class Delete(LoginRequiredMixin, OrganizationPermission, generic.DetailView):
    pass









