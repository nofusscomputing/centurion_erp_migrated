from django.shortcuts import render
from django.views import generic


class ProjectIndex(generic.View):

    permission_required = 'itam.view_device'

    template_name = 'form.html.j2'


    def get(self, request):

        context = {}

        context['content_title'] = 'Project Management'

        return render(request, self.template_name, context)
