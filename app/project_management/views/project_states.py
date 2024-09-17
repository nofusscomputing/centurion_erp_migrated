import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.models.ticket.ticket import Ticket
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from project_management.forms.project_state import DetailForm, ProjectState, ProjectStateForm

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = ProjectStateForm

    model = ProjectState

    permission_required = [
        'project_management.add_projectstate',
    ]


    def get_initial(self):

        initial: dict = {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }

        return initial


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_states')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class Change(ChangeView):

    context_object_name = "project_task"

    form_class = ProjectStateForm

    model = ProjectState

    permission_required = [
        'project_management.change_projectstate',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.title

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_state_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = ProjectState
    
    permission_required = [
        'project_management.delete_projectstate',
    ]
    
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_states')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context



class Index(IndexView):

    model = ProjectState

    permission_required = [
        'project_management.view_projectstate',
    ]

    template_name = 'project_management/project_state_index.html.j2'

    context_object_name = "project_states"

    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Project States'

        return context


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.model.objects.filter().order_by('name')

        else:

            return self.model.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



class View(ChangeView):

    model = ProjectState

    permission_required = [
        'project_management.view_projectstate'
    ]

    template_name = 'project_management/project_state.html.j2'

    form_class = DetailForm

    context_object_name = "project"



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Settings:_project_state_delete', kwargs={'pk': self.kwargs['pk']})

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
