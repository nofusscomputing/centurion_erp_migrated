from django.shortcuts import render
from django.views import generic

from .models import Organization, Team


class IndexView(generic.ListView):
    # model = Organization
    template_name = 'structure/index.html.j2'

    context_object_name = "organization_list"

    def get_queryset(self):

        return Organization.objects.filter(team=None)
