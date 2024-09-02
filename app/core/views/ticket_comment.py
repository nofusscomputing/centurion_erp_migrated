import markdown

from django.urls import reverse
from django.views import generic

from django_celery_results.models import TaskResult

from access.mixin import OrganizationPermission

from core.forms.ticket_comment import CommentForm, DetailForm
from core.models.ticket.ticket_comment import TicketComment, Ticket
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = CommentForm

    model = TicketComment

    parent_model = Ticket

    parent_model_pk_kwarg = 'ticket_id'

    template_name = 'form.html.j2'


    def get_dynamic_permissions(self):

        return [
            str('core.add_ticketcomment'),
        ]


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_initial(self):

        initial_values: dict = {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization,
            'type_ticket': self.kwargs['ticket_type'],
            'ticket': self.kwargs['ticket_id'],
        }

        if 'comment_type' in self.request.GET:

            initial_values.update({
                'qs_comment_type': self.request.GET['comment_type']
            })

        if 'parent_id' in self.kwargs:

            initial_values.update({
                'parent': self.kwargs['parent_id']
            })

        return initial_values


    def get_success_url(self, **kwargs):

        if self.kwargs['ticket_type'] == 'request':
            return reverse('Assistance:_ticket_request_view', args=(self.kwargs['ticket_type'],self.kwargs['ticket_id']))

        return f"/ticket/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Ticket Comment'

        return context



class Change(ChangeView):

    form_class = CommentForm

    model = TicketComment



    def get_dynamic_permissions(self):

        return [
            str('core.change_ticketcomment'),
        ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = str(self.object)

        return context


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_initial(self):
        return {
            'type_ticket': self.kwargs['ticket_type'],
        }


    def get_success_url(self, **kwargs):

        return reverse('Assistance:_ticket_request_view', args=(self.kwargs['ticket_type'], self.kwargs['ticket_id'],))
