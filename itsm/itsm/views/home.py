import requests

from django.shortcuts import render
from django.views.generic import View

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):

        context = {}

        return render(request, self.template_name, context)


