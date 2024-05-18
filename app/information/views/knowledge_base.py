import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from access.mixin import OrganizationPermission



class Index(generic.View):

    # permission_required = [
    #     'itil.view_knowledge_base'
    # ]

    template_name = 'base.html.j2'
 
    def get(self, request):
        context = {}

        context['content_title'] = 'Knowledge Base'

        return render(request, self.template_name, context)
