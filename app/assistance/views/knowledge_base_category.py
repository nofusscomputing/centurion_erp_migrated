from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from assistance.forms.knowledge_base_category import KnowledgeBaseCategoryForm
from assistance.models.knowledge_base import KnowledgeBase, KnowledgeBaseCategory

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from settings.models.user_settings import UserSettings



class Index(IndexView):

    context_object_name = "items"

    model = KnowledgeBaseCategory

    paginate_by = 10

    permission_required = [
        'assistance.view_knowledgebasecategory'
    ]

    template_name = 'assistance/kb_category_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/knowledge_base/'

        context['content_title'] = 'Knowledge Base Categories'

        return context


class Add(AddView):

    form_class = KnowledgeBaseCategoryForm

    model = KnowledgeBaseCategory

    permission_required = [
        'assistance.add_knowledgebasecategory',
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

        return reverse('Settings:KB Categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class Change(ChangeView):

    context_object_name = "group"

    form_class = KnowledgeBaseCategoryForm

    model = KnowledgeBaseCategory

    permission_required = [
        'assistance.change_knowledgebasecategory',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_knowledge_base_category_view', args=(self.kwargs['pk'],))



class View(ChangeView):

    context_object_name = "item"

    form_class = KnowledgeBaseCategoryForm

    model = KnowledgeBaseCategory

    permission_required = [
        'assistance.view_knowledgebasecategory',
    ]

    template_name = 'assistance/kb_category.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['articles'] = KnowledgeBase.objects.filter(category=self.kwargs['pk'])

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('Settings:_knowledge_base_category_delete', args=(self.kwargs['pk'],))


        context['content_title'] = self.object.name

        return context


    @method_decorator(auth_decorator.permission_required("assistance.change_knowledgebasecategory", raise_exception=True))
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

        return reverse('Settings:_knowledge_base_category_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = KnowledgeBaseCategory

    permission_required = [
        'assistance.delete_knowledgebasecategory',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:KB Categories')
