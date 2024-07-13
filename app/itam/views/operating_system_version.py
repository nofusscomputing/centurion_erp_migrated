from django.urls import reverse

from core.views.common import AddView, ChangeView, DeleteView

from itam.forms.operating_system_version import OperatingSystemVersionForm
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class View(ChangeView):

    form_class = OperatingSystemVersionForm

    model = OperatingSystemVersion

    permission_required = [
        'itam.view_operating_systemversion'
    ]

    template_name = 'form.html.j2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.operating_system.name + ' ' + self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['operating_system_id'],))



class Add(AddView):

    form_class = OperatingSystemVersionForm

    model = OperatingSystemVersion

    permission_required = [
        'access.add_operating_systemversion',
    ]

    template_name = 'form.html.j2'

    def form_valid(self, form):
        operating_system = OperatingSystem.objects.get(pk=self.kwargs['pk'])

        form.instance.is_global = operating_system.is_global
        form.instance.organization_id = operating_system.organization.id
        form.instance.operating_system_id = self.kwargs['pk']
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['pk'],))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Operating System Version'

        return context



class Delete(DeleteView):
    model = OperatingSystemVersion
    permission_required = [
        'access.delete_operating_system',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('ITAM:_operating_system_view', args=(self.kwargs['operating_system_id'],))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
