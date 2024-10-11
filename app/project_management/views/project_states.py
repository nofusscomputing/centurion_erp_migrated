from django.urls import reverse

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from project_management.forms.project_states import DetailForm, ProjectState, ProjectStateForm

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = ProjectStateForm

    model = ProjectState

    permission_required = [
        'project_management.add_projectstate',
    ]


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_states')



class Change(ChangeView):

    context_object_name = "project_state"

    form_class = ProjectStateForm

    model = ProjectState

    permission_required = [
        'project_management.change_projectstate',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_state_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = ProjectState

    permission_required = [
        'project_management.delete_projectstate',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_project_states')



class Index(IndexView):

    context_object_name = "project_states"

    model = ProjectState

    paginate_by = 10

    permission_required = [
        'project_management.view_projectstate'
    ]

    template_name = 'project_management/project_state_index.html.j2'



class View(ChangeView):

    context_object_name = "project_state"

    form_class = DetailForm

    model = ProjectState

    permission_required = [
        'project_management.view_projectstate',
    ]

    template_name = 'project_management/project_state.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('Settings:_project_state_delete', args=(self.kwargs['pk'],))


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

        return reverse('Settings:_project_state_view', args=(self.kwargs['pk'],))
