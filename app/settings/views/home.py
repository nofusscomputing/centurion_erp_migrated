import requests

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import View

from settings.models.settings import Settings

class View(View):

    permission_required = 'itam.view_settings'
    template_name = 'settings/home.html.j2'


    def get(self, request):

        context = {}

        context['content_title'] = 'Settings'

        return render(request, self.template_name, context)
