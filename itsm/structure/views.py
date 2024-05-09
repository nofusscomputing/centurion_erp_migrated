from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from .models import Organization, Team


class IndexView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'organization.view_organization'
    template_name = 'structure/index.html.j2'
    context_object_name = "organization_list"


    def get_queryset(self):

        return Organization.objects.filter(team=None)


class OrganizationView(PermissionRequiredMixin, generic.DetailView):
    model = Organization
    template_name = "structure/organization.html.j2"
    permission_required = 'organization.view_organization'


    def get_queryset(self):

        return Organization.objects.filter()
