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
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from project_management.forms.project import ProjectForm
from project_management.models.projects import Project

from settings.models.user_settings import UserSettings



class ProjectIndex(IndexView):

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



class ProjectView(ChangeView):

    model = Project

    permission_required = [
        'itam.view_device',
        'itam.change_device'
    ]

    template_name = 'project_management/project.html.j2'

    form_class = ProjectForm

    context_object_name = "project"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # context['notes_form'] = AddNoteForm(prefix='note')
        # context['notes'] = Notes.objects.filter(project=self.kwargs['pk'])


        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Project Management:_project_delete', args=(self.kwargs['pk'],))

        context['content_title'] = context['project'].name

        return context


    # def post(self, request, *args, **kwargs):

    #     project = self.model.objects.get(pk=self.kwargs['pk'])

    #     notes = AddNoteForm(request.POST, prefix='note')

    #     if notes.is_bound and notes.is_valid() and notes.instance.note != '':

    #         if request.user.has_perm('core.add_notes'):

    #             notes.instance.organization = device.organization
    #             notes.instance.project = project
    #             notes.instance.usercreated = request.user

    #             notes.save()

    #     return super().post(request, *args, **kwargs)



class ProjectAdd(AddView):

    form_class = ProjectForm

    model = Project

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



class ProjectChange(ChangeView):

    form_class = ProjectForm

    model = Project

    permission_required = [
        'project_management.change_project',
    ]

    template_name = 'form.html.j2'


    def form_valid(self, form):
        form.instance.is_global = False
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('Project Management:_project_view', kwargs={'pk': self.kwargs['pk']})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Edit'

        return context



class ProjectDelete(DeleteView):
    model = Project
    
    permission_required = [
        'project_management.delete_project',
    ]
    
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Project Management:Projects')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context

