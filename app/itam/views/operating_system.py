from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from core.forms.comment import AddNoteForm
from core.models.notes import Notes

from itam.models.device import DeviceOperatingSystem
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion
from itam.forms.operating_system.update import Update



class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    model = OperatingSystem
    permission_required = 'itam.view_operating_system'
    template_name = 'itam/operating_system_index.html.j2'
    context_object_name = "operating_systems"
    paginate_by = 10


    def get_queryset(self):

        if self.request.user.is_superuser:

            return OperatingSystem.objects.filter().order_by('name')

        else:

            return OperatingSystem.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')



class View(OrganizationPermission, generic.UpdateView):
    model = OperatingSystem
    permission_required = [
        'itam.view_operating_system'
    ]
    template_name = 'itam/operating_system.html.j2'

    form_class = Update

    context_object_name = "operating_system"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        operating_system_versions = OperatingSystemVersion.objects.filter(operating_system=self.kwargs['pk']).order_by('name').annotate(installs=Count("deviceoperatingsystem"))
        context['operating_system_versions'] = operating_system_versions

        installs = DeviceOperatingSystem.objects.filter(operating_system_version__operating_system_id=self.kwargs['pk'])
        context['installs'] = installs

        context['notes_form'] = AddNoteForm(prefix='note')

        context['notes'] = Notes.objects.filter(operatingsystem=self.kwargs['pk'])

        context['content_title'] = self.object.name

        return context


    def post(self, request, *args, **kwargs):

        operatingsystem = OperatingSystem.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid():

            notes.instance.organization = operatingsystem.organization
            notes.instance.operatingsystem = operatingsystem
            notes.instance.usercreated = request.user

            notes.save()

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['pk'],))



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = OperatingSystem
    permission_required = [
        'access.add_operating_system',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name',
        'organization',
        'is_global'
    ]


    def get_success_url(self, **kwargs):

        return reverse('ITAM:Operating Systems')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Operating System'

        return context



class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):

    model = OperatingSystem

    permission_required = [
        'access.delete_operating_system',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('ITAM:Operating Systems')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
