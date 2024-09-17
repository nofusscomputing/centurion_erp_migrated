from datetime import datetime

from django.contrib.auth import decorators as auth_decorator
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator

from access.models import TeamUsers

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from project_management.forms.project_types import DetailForm, ProjectType, ProjectTypeForm

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = ProjectTypeForm

    model = ProjectType

    permission_required = [
        'project_management.add_projecttype',
    ]


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_types')



class Change(ChangeView):

    context_object_name = "project_type"

    form_class = ProjectTypeForm

    model = ProjectType

    permission_required = [
        'project_management.change_projecttype',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_type_view', args=(self.kwargs['pk'],))



class Index(IndexView):

    context_object_name = "project_types"

    model = ProjectType

    paginate_by = 10

    permission_required = [
        'project_management.view_projecttype'
    ]

    template_name = 'project_management/project_type_index.html.j2'



class View(ChangeView):

    context_object_name = "project_type"

    form_class = DetailForm

    model = ProjectType

    permission_required = [
        'project_management.view_projecttype',
    ]

    template_name = 'project_management/project_type.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('Settings:_project_type_delete', args=(self.kwargs['pk'],))


        context['content_title'] = self.object.name

        return context


    def post(self, request, *args, **kwargs):

        item = KnowledgeBase.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = item.organization

            notes.save()

        # dont allow saving any post data outside notes.
        # todo: figure out what needs to be returned
        # return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_type_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = ProjectType

    permission_required = [
        'project_management.delete_projecttype',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_types')
