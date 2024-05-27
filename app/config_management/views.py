from django.shortcuts import render
from django.views import generic


class ConfigIndex(generic.View):

    permission_required = 'itam.view_device'

    template_name = 'form.html.j2'


    def get(self, request):

        context = {}

        context['content_title'] = 'Config Management'

        return render(request, self.template_name, context)
