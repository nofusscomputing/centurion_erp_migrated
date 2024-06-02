from django.contrib.auth import decorators as auth_decorator

from django.db.models import Count, Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from access.mixin import OrganizationPermission

from core.forms.comment import AddNoteForm
from core.models.notes import Notes

from settings.models.user_settings import UserSettings

from config_management.models.groups import ConfigGroups



class GroupIndexView(OrganizationPermission, generic.ListView):

    context_object_name = "groups"

    model = ConfigGroups

    paginate_by = 10

    permission_required = 'config_management.view_groups'

    template_name = 'config_management/group_index.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Config Groups'

        return context


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.model.objects.filter(parent=None).order_by('name')

        else:

            return self.model.objects.filter(Q(parent=None, organization__in=self.user_organizations()) | Q(parent=None, is_global = True)).order_by('name')




class GroupAdd(OrganizationPermission, generic.CreateView):

    fields = [
        'name',
        'parent',
        'organization',
    ]

    model = ConfigGroups

    permission_required = [
        'config_management.add_groups',
    ]

    template_name = 'form.html.j2'


    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'New Group'

        return context



class GroupView(OrganizationPermission, generic.UpdateView):

    context_object_name = "group"

    model = ConfigGroups

    permission_required = [
        'config_management.view_groups',
    ]

    template_name = 'config_management/group.html.j2'

    fields = [
        'name',
        'parent',
        'config',
    ]


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['child_groups'] = ConfigGroups.objects.filter(parent=self.kwargs['pk'])

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(config_group=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Config Management:_group_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

#         if self.request.user.is_superuser:

#             context['device_software'] = DeviceSoftware.objects.filter(
#                 software=self.kwargs['pk']
#             ).order_by(
#                 'device',
#                 'organization'
#             )

#         elif not self.request.user.is_superuser:
#             context['device_software'] = DeviceSoftware.objects.filter(
#                 Q(device__in=self.user_organizations(),
#                 software=self.kwargs['pk'])
#             ).order_by(
#                 'device',
#                 'organization'
#             )

        return context


    @method_decorator(auth_decorator.permission_required("itam.change_software", raise_exception=True))
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



class GroupDelete(OrganizationPermission, generic.DeleteView):

    model = ConfigGroups

    permission_required = [
        'config_management.delete_groups',
    ]

    template_name = 'form.html.j2'

    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
