import json

from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.models.ticket.ticket_linked_items import Ticket, TicketLinkedItem
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itam.models.device import Device

from settings.models.user_settings import UserSettings

from config_management.forms.group.group import ConfigGroupForm, DetailForm
from config_management.models.groups import ConfigGroups, ConfigGroupSoftware



class Index(IndexView):

    context_object_name = "groups"

    model = ConfigGroups

    paginate_by = 10

    permission_required = [
        'config_management.view_configgroups'
    ]

    template_name = 'config_management/group_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/'

        context['content_title'] = 'Config Groups'

        return context


    def get_queryset(self):

        return self.model.objects.filter(parent=None).order_by('name')



class Add(AddView):

    organization_field = 'organization'

    form_class = ConfigGroupForm

    model = ConfigGroups

    permission_required = [
        'config_management.add_configgroups',
    ]

    template_name = 'form.html.j2'


    def get_initial(self):

        # initial: dict = {
        #     'organization': UserSettings.objects.get(user = self.request.user).default_organization
        # }

        initial = super().get_initial()

        if 'pk' in self.kwargs:

            if self.kwargs['pk']:

                initial.update({'parent': self.kwargs['pk']})

                self.model.parent.field.hidden = True

        return initial


    def get_success_url(self, **kwargs):

        if 'group_id' in self.kwargs:

            if self.kwargs['group_id']:

                return reverse('Config Management:_group_view', args=(self.kwargs['group_id'],))

        return reverse('Config Management:Groups')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class Change(ChangeView):

    context_object_name = "group"

    form_class = ConfigGroupForm

    model = ConfigGroups

    permission_required = [
        'config_management.change_configgroups',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=(self.kwargs['pk'],))



class View(ChangeView):

    context_object_name = "group"

    form_class = DetailForm

    model = ConfigGroups

    permission_required = [
        'config_management.view_configgroups',
    ]

    template_name = 'config_management/group.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['child_groups'] = ConfigGroups.objects.filter(parent=self.kwargs['pk'])

        context['config'] = json.dumps(self.object.render_config(), indent=4, sort_keys=True)


        context['tickets'] = TicketLinkedItem.objects.filter(
            item = int(self.kwargs['pk']),
            item_type = TicketLinkedItem.Modules.CONFIG_GROUP
        )

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Config Management:_group_delete', args=(self.kwargs['pk'],))

        softwares = ConfigGroupSoftware.objects.filter(config_group=self.kwargs['pk'])[:50]
        context['softwares'] = softwares

        context['content_title'] = self.object.name

        # if self.request.user.is_superuser:

        #     context['device_software'] = DeviceSoftware.objects.filter(
        #         software=self.kwargs['pk']
        #     ).order_by(
        #         'device',
        #         'organization'
        #     )

        # elif not self.request.user.is_superuser:
        #     context['device_software'] = DeviceSoftware.objects.filter(
        #         Q(device__in=self.user_organizations(),
        #         software=self.kwargs['pk'])
        #     ).order_by(
        #         'device',
        #         'organization'
        #     )

        return context


    @method_decorator(auth_decorator.permission_required("config_management.change_configgroups", raise_exception=True))
    def post(self, request, *args, **kwargs):

        item = ConfigGroups.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = item.organization
            notes.instance.config_group = item
            notes.instance.usercreated = request.user

            notes.save()

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=(self.kwargs['pk'],))



class Delete(DeleteView):

    model = ConfigGroups

    permission_required = [
        'config_management.delete_configgroups',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Config Management:Groups')
