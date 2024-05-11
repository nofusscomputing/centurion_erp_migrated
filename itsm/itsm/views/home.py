import requests

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import View


class HomeView(View):
    template_name = 'home.html.j2'


    def get(self, request):
        if not request.user.is_authenticated and settings.LOGIN_REQUIRED:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        context = {}

        return render(request, self.template_name, context)
