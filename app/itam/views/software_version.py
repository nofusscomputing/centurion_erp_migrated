from core.views.common import AddView, ChangeView

from ..models.software import Software, SoftwareVersion


class View(ChangeView):
    model = SoftwareVersion
    permission_required = [
        'itam.view_softwareversion'
    ]
    template_name = 'form.html.j2'

    fields = [
        "name",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return f"/itam/software/{self.kwargs['software_id']}/"



class Add(AddView):
    model = SoftwareVersion
    permission_required = [
        'access.add_softwareversion',
    ]
    template_name = 'form.html.j2'
    fields = [
        'name'
    ]

    def form_valid(self, form):
        software = Software.objects.get(pk=self.kwargs['pk'])

        form.instance.is_global = software.is_global
        form.instance.organization_id = software.organization.id
        form.instance.software_id = self.kwargs['pk']
        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return f"/itam/software/{self.kwargs['pk']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software Version'

        return context
