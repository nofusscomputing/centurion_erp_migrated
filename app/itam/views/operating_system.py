from django.contrib.auth import decorators as auth_decorator
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.models.ticket.ticket_linked_items import Ticket, TicketLinkedItem
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itam.models.device import DeviceOperatingSystem
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.forms.operating_system.update import DetailForm, OperatingSystemForm

from settings.models.user_settings import UserSettings



class Add(AddView):

    form_class = OperatingSystemForm

    model = OperatingSystem

    permission_required = [
        'itam.add_operatingsystem',
    ]

    template_name = 'form.html.j2'


    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return reverse('ITAM:Operating Systems')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Operating System'

        return context



class Change(ChangeView):

    context_object_name = "operating_system"

    form_class = OperatingSystemForm

    model = OperatingSystem

    permission_required = [
        'itam.change_operatingsystem',
    ]

    template_name = 'form.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context


    @method_decorator(auth_decorator.permission_required("itam.change_operatingsystem", raise_exception=True))
    def post(self, request, *args, **kwargs):

        operatingsystem = OperatingSystem.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = operatingsystem.organization
            notes.instance.operatingsystem = operatingsystem
            notes.instance.usercreated = request.user

            notes.save()

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = OperatingSystem

    permission_required = [
        'itam.delete_operatingsystem',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('ITAM:Operating Systems')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['content_title'] = 'Delete ' + self.object.name

        return context



class IndexView(IndexView):
    model = OperatingSystem
    permission_required = [
        'itam.view_operatingsystem'
    ]
    template_name = 'itam/operating_system_index.html.j2'
    context_object_name = "operating_systems"
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/operating_system/'

        return context


    def get_queryset(self):

        if self.request.user.is_superuser:

            return OperatingSystem.objects.filter().order_by('name')

        else:

            return OperatingSystem.objects.filter().order_by('name')



class View(ChangeView):

    context_object_name = "operating_system"

    form_class = DetailForm

    model = OperatingSystem

    permission_required = [
        'itam.view_operatingsystem',
    ]

    template_name = 'itam/operating_system.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        operating_system_versions = OperatingSystemVersion.objects.filter(
            operating_system=self.kwargs['pk']
        ).order_by(
            'name'
        ).annotate(
            installs=Count(
                "deviceoperatingsystem",
                filter=Q(deviceoperatingsystem__device__organization__in = self.user_organizations())
            ),
            # filter=Q(deviceoperatingsystem__operating_system_version__organization__in = self.user_organizations())
            # filter=Q(deviceoperatingsystem__operating_system_version__deviceoperatingsystem__device__organization__in = self.user_organizations()),
            filter=Q(deviceoperatingsystem__operating_system_version__organization__in = self.user_organizations()),
            
        )
        
        context['operating_system_versions'] = operating_system_versions

        context['tickets'] = TicketLinkedItem.objects.filter(
            item = int(self.kwargs['pk']),
            item_type = TicketLinkedItem.Modules.OPERATING_SYSTEM
        )

        installs = DeviceOperatingSystem.objects.filter(operating_system_version__operating_system_id=self.kwargs['pk'])
        context['installs'] = installs

        context['notes_form'] = AddNoteForm(prefix='note')

        context['notes'] = Notes.objects.filter(operatingsystem=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('ITAM:_operating_system_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context


    # @method_decorator(auth_decorator.permission_required("itam.change_operatingsystem", raise_exception=True))
    def post(self, request, *args, **kwargs):

        operatingsystem = OperatingSystem.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = operatingsystem.organization
            notes.instance.operatingsystem = operatingsystem
            notes.instance.usercreated = request.user

            notes.save()

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['pk'],))
