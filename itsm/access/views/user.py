from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from access.mixin import OrganizationPermission
from access.models import Team, TeamUsers



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = TeamUsers
    permission_required = [
        'access.view_team',
        'access.add_teamusers'
    ]
    template_name = 'form.html.j2'
    fields = [
        'user',
        'manager'
    ]


    def form_valid(self, form):
        form.instance.team = Team.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['organization_id']}/team/{self.kwargs['pk']}"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Team User'

        return context


class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = TeamUsers
    permission_required = [
        'access.view_team',
        'access.delete_teamusers'
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['organization_id']}/team/{self.kwargs['team_id']}"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete Team User'

        return context
