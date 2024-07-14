import json

from django.db.models import Q
from django.shortcuts import render
from django.template import Template, Context
from django.views import generic

from access.mixin import OrganizationPermission



class Index(generic.View):

    # permission_required = [
    #     'itil.view_playbook'
    # ]

    template_name = 'form.html.j2'

    def get(self, request):
        context = {}

        user_string = Template("{% include 'icons/issue_link.html.j2' with issue=11 %}")
        user_context = Context(context)
        context['form'] = user_string.render(user_context)

        context['content_title'] = 'Playbooks'

        return render(request, self.template_name, context)
