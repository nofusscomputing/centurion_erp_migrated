from django.contrib.auth import decorators as auth_decorator
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.forms.comment import AddNoteForm
from core.models.notes import Notes
from core.views.common import AddView, ChangeView, DeleteView, IndexView

from itam.models.device import DeviceSoftware
from itam.models.software import Software, SoftwareVersion
from itam.forms.software.update import SoftwareForm, SoftwareFormUpdate

from settings.models.user_settings import UserSettings



class IndexView(IndexView):

    context_object_name = "softwares"

    model = Software

    paginate_by = 10

    permission_required = [
        'itam.view_software'

    ]

    template_name = 'itam/software_index.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'

        return context


    def get_queryset(self):

        if self.request.user.is_superuser:

            return Software.objects.filter().order_by('name')

        else:

            return Software.objects.filter().order_by('name')



class View(ChangeView):

    context_object_name = "software"

    form_class = SoftwareFormUpdate

    model = Software

    permission_required = [
        'itam.view_software',
        'itam.change_software'
    ]

    template_name = 'itam/software.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        software_versions = SoftwareVersion.objects.filter(
            software=self.kwargs['pk'],
        ).annotate(
            installs=Count(
                "installedversion", 
                filter=Q(installedversion__organization__in = self.user_organizations())
            )
        )

        context['software_versions'] = software_versions

        context['notes_form'] = AddNoteForm(prefix='note')
        context['notes'] = Notes.objects.filter(software=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('ITAM:_software_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        if self.request.user.is_superuser:

            context['device_software'] = DeviceSoftware.objects.filter(
                software=self.kwargs['pk']
            ).order_by(
                'device',
                'organization'
            )

        elif not self.request.user.is_superuser:

            context['device_software'] = DeviceSoftware.objects.filter(
                software=self.kwargs['pk']
            ).order_by(
                'device',
                'organization'
            )

        return context


    @method_decorator(auth_decorator.permission_required("itam.change_software", raise_exception=True))
    def post(self, request, *args, **kwargs):

        software = Software.objects.get(pk=self.kwargs['pk'])

        notes = AddNoteForm(request.POST, prefix='note')

        if notes.is_bound and notes.is_valid() and notes.instance.note != '':

            notes.instance.organization = software.organization
            notes.instance.software = software
            notes.instance.usercreated = request.user

            notes.save()



        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return f"/itam/software/{self.kwargs['pk']}/"



class Add(AddView):

    form_class = SoftwareForm

    model = Software

    permission_required = [
        'itam.add_software',
    ]

    template_name = 'form.html.j2'


    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return f"/itam/software/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software'

        return context

class Delete(DeleteView):
    model = Software
    permission_required = [
        'itam.delete_software',
    ]
    template_name = 'form.html.j2'

    def get_success_url(self, **kwargs):

        return f"/itam/software/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
