import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.models.ticket import Ticket
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from project_management.forms.project_milestone import DetailForm, ProjectMilestone, ProjectMilestoneForm

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = ProjectMilestoneForm

    model = ProjectMilestone

    permission_required = [
        'project_management.add_projectmilestone',
    ]

    template_name = 'form.html.j2'
    

    def get_initial(self):
        initial = super().get_initial()

        initial.update({
            'project': self.kwargs['project_id']
        })

        return initial

    def form_valid(self, form):
        form.instance.is_global = False
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('Project Management:_project_view', kwargs={'pk': self.kwargs['project_id']}) + '?tab=milestones'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Create a Project Milestone'

        return context



class Change(ChangeView):

    form_class = ProjectMilestoneForm

    model = ProjectMilestone

    permission_required = [
        'project_management.change_projectmilestone',
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



class Delete(DeleteView):

    model = ProjectMilestone
    
    permission_required = [
        'project_management.delete_projectmilestone',
    ]
    
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Project Management:_project_view', kwargs={'pk': self.kwargs['project_id']}) + '?tab=milestones'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context



class View(ChangeView):

    model = ProjectMilestone

    permission_required = [
        'project_management.view_projectmilestone'
    ]

    template_name = 'project_management/project_milestone.html.j2'

    form_class = DetailForm

    context_object_name = "project"


    def get_initial(self):
        initial = super().get_initial()

        initial.update({
            'project': self.kwargs['project_id']
        })

        return initial


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['tasks'] = Ticket.objects.filter(
            project = self.object.project,
            milestone = self.kwargs['pk'],
        )

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Project Management:_project_milestone_delete', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['pk']})

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
