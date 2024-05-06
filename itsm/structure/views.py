from django.shortcuts import render
from django.views import generic

from .models import Organization, Team


class IndexView(generic.ListView):
    # model = Organization
    template_name = 'structure/index.html.j2'

    context_object_name = "organization_list"

    def get_queryset(self):

        return Organization.objects.filter(team=None)


class OrganizationView(generic.DetailView):
    model = Organization
    template_name = "structure/organization.html.j2"

    # context_object_name = Team


    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Organization.objects.filter()
