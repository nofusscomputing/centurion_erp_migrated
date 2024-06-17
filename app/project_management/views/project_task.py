import json
import markdown

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from core.forms.comment import AddNoteForm
from core.models.notes import Notes

from project_management.models.project_tasks import ProjectTask

from settings.models.user_settings import UserSettings



class ProjectTaskAdd(generic.CreateView):

    # form_class = ProjectForm

    model = ProjectTask

    permission_required = [
        'project_management.add_project',
    ]

    template_name = 'form.html.j2'
    

    def get_initial(self):
        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }

    def form_valid(self, form):
        form.instance.is_global = False
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('Project Management:Projects')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Create a Project'

        return context
