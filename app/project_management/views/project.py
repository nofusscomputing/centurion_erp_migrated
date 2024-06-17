import json
import markdown

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from project_management.forms.project import ProjectForm
from project_management.models.projects import Project

from settings.models.user_settings import UserSettings



class ProjectIndex(OrganizationPermission, generic.ListView):

    model = Project

    permission_required = 'project_management.view_project'

    template_name = 'project_management/project_index.html.j2'

    context_object_name = "projects"

    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Projects'

        return context


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.model.objects.filter().order_by('name')

        else:

            return self.model.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')

        return context

        return context
