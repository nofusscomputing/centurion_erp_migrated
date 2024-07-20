from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itim.forms.ports import PortForm
from itim.models.services import Port

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = PortForm

    model = Port

    permission_required = [
        'itam.add_service',
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

        return reverse('Settings:_ports')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class Index(IndexView):

    context_object_name = "items"

    model = Port

    paginate_by = 10

    permission_required = [
        'assistance.view_service'
    ]

    template_name = 'itim/port_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + self.model._meta.model_name

        context['content_title'] = 'Ports'

        return context
