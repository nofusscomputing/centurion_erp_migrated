from django.urls import reverse

from itam.models.software import Software

from config_management.forms.group.add_software import SoftwareAdd
from config_management.forms.group.change_software import SoftwareUpdate
from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from core.views.common import AddView, ChangeView, DeleteView


class GroupSoftwareAdd(AddView):

    form_class = SoftwareAdd

    model = ConfigGroupSoftware

    parent_model = ConfigGroups

    permission_required = [
        'config_management.add_configgroupsoftware',
    ]

    template_name = 'form.html.j2'


    def form_valid(self, form):
        config_group = ConfigGroups.objects.get(pk=self.kwargs['pk'])
        form.instance.organization_id = config_group.organization.id
        form.instance.config_group = config_group

        software = Software.objects.get(pk=form.instance.software.id)

        if ConfigGroupSoftware.objects.filter(
            config_group=config_group,
            software=software
        ).exists():

            existing_object = ConfigGroupSoftware.objects.get(
                device=device,
                software=software
            )

            existing_object.action = form.instance.action
            existing_object.save()

            return HttpResponseRedirect(self.get_success_url())
        
        else:

            return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=(self.kwargs['pk'],))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software Action'

        return context



class GroupSoftwareChange(ChangeView):

    form_class = SoftwareUpdate

    model = ConfigGroupSoftware

    permission_required = [
        'config_management.change_configgroupsoftware'

    ]

    template_name = 'form.html.j2'


    def form_valid(self, form):
        config_group = ConfigGroups.objects.get(pk=self.kwargs['group_id'])

        form.instance.organization_id = config_group.organization.id
        form.instance.config_group = config_group

        return super().form_valid(form)


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=(self.kwargs['group_id'],))

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_delete_url'] = reverse('Config Management:_group_software_delete', args=(self.kwargs['group_id'], self.kwargs['pk'],))

        context['content_title'] = 'Edit Software Action'

        return context



class GroupSoftwareDelete(DeleteView):

    model = ConfigGroupSoftware

    permission_required = [
        'config_management.delete_configgroupsoftware',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Config Management:_group_view', args=(self.kwargs['group_id'],))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete '

        return context
