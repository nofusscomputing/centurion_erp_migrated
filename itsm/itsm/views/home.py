import requests

from django.shortcuts import render
from django.views.generic import View

class HomeView(View):
    template_name = 'home.html.j2'

    def get(self, request):

        context = {}

        return render(request, self.template_name, context)


