from datetime import datetime

from django.contrib.auth import decorators as auth_decorator
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator

from access.models import TeamUsers

from assistance.forms.knowledge_base import KnowledgeBaseForm
from assistance.models.knowledge_base import KnowledgeBase

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from settings.models.user_settings import UserSettings



class Index(IndexView):

    context_object_name = "items"

    model = KnowledgeBase

    paginate_by = 10

    permission_required = [
        'assistance.view_knowledgebase'
    ]

    template_name = 'assistance/kb_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if not self.request.user.has_perm('assistance.change_knowledgebase') and not self.request.user.is_superuser:

            user_teams = []
            for team_user in TeamUsers.objects.filter(user=self.request.user):

                if team_user.team.id not in user_teams:

                    user_teams += [ team_user.team.id ]


            context['items'] = self.get_queryset().filter(
                Q(expiry_date__lte=datetime.now())
                  |
                Q(expiry_date=None)
            ).filter(
                Q(target_team__in=user_teams)
                  |
                Q(target_user=self.request.user.id)
            ).distinct()

        context['model_docs_path'] = self.model._meta.app_label + '/knowledge_base/'

        context['content_title'] = 'Knowledge Base Articles'

        return context



class Add(AddView):

    form_class = KnowledgeBaseForm

    model = KnowledgeBase

    permission_required = [
        'assistance.add_knowledgebase',
    ]


    def get_initial(self):

        initial: dict = {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }

        if 'pk' in self.kwargs:

            if self.kwargs['pk']:

                initial.update({'parent': self.kwargs['pk']})

                self.model.parent.field.hidden = True

        return initial


    def get_success_url(self, **kwargs):

        return reverse('Assistance:Knowledge Base')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class Change(ChangeView):

    context_object_name = "group"

    form_class = KnowledgeBaseForm

    model = KnowledgeBase

    permission_required = [
        'assistance.change_knowledgebase',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.title

        return context


    def get_success_url(self, **kwargs):

        return reverse('Assistance:_knowledge_base_view', args=(self.kwargs['pk'],))



class View(ChangeView):

    context_object_name = "kb"

    form_class = KnowledgeBaseForm

    model = KnowledgeBase

    permission_required = [
        'assistance.view_knowledgebase',
    ]

    template_name = 'assistance/kb_article.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('Assistance:_knowledge_base_delete', args=(self.kwargs['pk'],))


        context['content_title'] = self.object.title

        return context


    @method_decorator(auth_decorator.permission_required("assistance.change_knowledgebase", raise_exception=True))
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

        return reverse('Assistance:_knowledge_base_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = KnowledgeBase

    permission_required = [
        'assistance.delete_knowledgebase',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.title

        return context


    def get_success_url(self, **kwargs):

        return reverse('Assistance:Knowledge Base')
