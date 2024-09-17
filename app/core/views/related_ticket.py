from django.urls import reverse
from django.views import generic

from django_celery_results.models import TaskResult

from access.mixin import OrganizationPermission

from core.forms.related_ticket import RelatedTicketForm
from core.models.ticket.ticket import RelatedTickets
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = RelatedTicketForm

    model = RelatedTickets

    permission_required = [
        'itam.add_device',
    ]

    template_name = 'form.html.j2'


    def get_initial(self):

        initial_values: dict = {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization,
            'from_ticket_id': self.kwargs['ticket_id'],
        }

        return initial_values


    def get_success_url(self, **kwargs):

        if self.kwargs['ticket_type'] == 'request':

            return reverse('Assistance:_ticket_request_view', args=(self.kwargs['ticket_type'],self.kwargs['ticket_id'],))

        elif self.kwargs['ticket_type'] == 'project_task':

            return reverse('Project Management:_project_task_view', args=(self.object.from_ticket_id.project.id, self.kwargs['ticket_type'],self.kwargs['ticket_id'],))

        else:

            return reverse('ITIM:_ticket_' + str(self.kwargs['ticket_type']).lower() + '_view', args=(self.kwargs['ticket_type'],self.kwargs['ticket_id'],))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Ticket Comment'

        return context



class Delete(DeleteView):

    model = RelatedTickets

    permission_required = [
        'itim.delete_cluster',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + str(self.object)

        return context


    def get_success_url(self, **kwargs):

        return reverse('ITIM:Clusters')
