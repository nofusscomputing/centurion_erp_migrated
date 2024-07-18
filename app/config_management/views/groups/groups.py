import json

from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itam.models.device import Device

from settings.models.user_settings import UserSettings

from config_management.forms.group_hosts import ConfigGroupHostsForm
from config_management.forms.group.group import ConfigGroupForm
from config_management.models.groups import ConfigGroups, ConfigGroupHosts, ConfigGroupSoftware



class GroupIndexView(IndexView):

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



class GroupAdd(AddView):

    organization_field = 'organization'

    form_class = ConfigGroupForm

    model = ConfigGroups

    permission_required = [
        'config_management.add_configgroups',
    ]

    template_name = 'form.html.j2'


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

        if 'group_id' in self.kwargs:

            if self.kwargs['group_id']:

                return reverse('Config Management:_group_view', args=(self.kwargs['group_id'],))

        return reverse('Config Management:Groups')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class GroupView(ChangeView):

    context_object_name = "group"

    form_class = ConfigGroupForm

    model = ConfigGroups

    permission_required = [
        'config_management.view_configgroups',
        'config_management.change_configgroups',
    ]

    template_name = 'config_management/group.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['child_groups'] = ConfigGroups.objects.filter(parent=self.kwargs['pk'])

        context['config'] = json.dumps(json.loads(self.object.render_config()), indent=4, sort_keys=True)

        context['config_group_hosts'] = ConfigGroupHosts.objects.filter(group_id = self.kwargs['pk']).order_by('-host')

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



class GroupDelete(DeleteView):

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



class GroupHostAdd(AddView):

    model = ConfigGroupHosts

    parent_model = ConfigGroups

    permission_required = [
        'config_management.add_configgrouphosts',
    ]

    template_name = 'form.html.j2'

    form_class = ConfigGroupHostsForm


    def form_valid(self, form):

        form.instance.group_id = self.kwargs['pk']

        form.instance.organization = self.parent_model.objects.get(pk=form.instance.group_id).organization

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Host to Group'

        return context


    def get_form(self, form_class=None):

        form_class = super().get_form(form_class=None)

        group = ConfigGroups.objects.get(pk=self.kwargs['pk'])

        exsting_group_hosts = ConfigGroupHosts.objects.filter(group=group)

        form_class.fields["host"].queryset = form_class.fields["host"].queryset.filter(
        ).exclude(
            id__in=exsting_group_hosts.values_list('host', flat=True)
        )


        return form_class


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=[self.kwargs['pk'],])



class GroupHostDelete(DeleteView):

    model = ConfigGroupHosts

    permission_required = [
        'config_management.delete_configgrouphosts',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.host.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=[self.kwargs['group_id'],])
