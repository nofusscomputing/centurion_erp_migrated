from django.urls import reverse

from core.forms.comment import AddNoteForm
from core.forms.ticket_comment_category import DetailForm, TicketCommentCategory, TicketCommentCategoryForm

from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, IndexView



class Add(AddView):

    form_class = TicketCommentCategoryForm

    model = TicketCommentCategory

    permission_required = [
        'core.add_ticketcommentcategory',
    ]


    def get_initial(self):

        initial =  super().get_initial()

        if 'pk' in self.kwargs:

            if self.kwargs['pk']:

                initial.update({'parent': self.kwargs['pk']})

                self.model.parent.field.hidden = True

        return initial


    def get_success_url(self, **kwargs):

        return reverse('Settings:_ticket_comment_categories')



class Change(ChangeView):

    form_class = TicketCommentCategoryForm

    model = TicketCommentCategory

    permission_required = [
        'core.change_ticketcommentcategory',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = str(self.object)

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_ticket_comment_category_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = TicketCommentCategory

    permission_required = [
        'core.delete_ticketcommentcategory',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + str(self.object)

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_ticket_comment_categories')



class Index(IndexView):

    context_object_name = "items"

    model = TicketCommentCategory

    paginate_by = 10

    permission_required = [
        'core.view_ticketcommentcategory'
    ]

    template_name = 'core/index_ticket_comment_categories.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/ticket_comment_category'

        return context



class View(ChangeView):

    context_object_name = "ticket_categories"

    form_class = DetailForm

    model = TicketCommentCategory

    permission_required = [
        'core.view_ticketcommentcategory',
    ]

    template_name = 'core/ticket_comment_category.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(service=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.model_name

        context['model_delete_url'] = reverse('Settings:_ticket_comment_category_delete', kwargs={'pk': self.kwargs['pk']})


        context['content_title'] = self.object.name

        return context


    # def post(self, request, *args, **kwargs):

    #     item = Cluster.objects.get(pk=self.kwargs['pk'])

    #     notes = AddNoteForm(request.POST, prefix='note')

    #     if notes.is_bound and notes.is_valid() and notes.instance.note != '':

    #         notes.instance.service = item

    #         notes.instance.organization = item.organization

    #         notes.save()


    def get_success_url(self, **kwargs):

        return reverse('Settings:_ticket_comment_category_view', kwargs={'pk': self.kwargs['pk']})
