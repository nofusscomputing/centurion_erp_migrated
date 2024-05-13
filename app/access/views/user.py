from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User, Group
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
        team = Team.objects.get(pk=self.kwargs['pk'])
        form.instance.team = team

        group = Group.objects.get(pk=team.group_ptr_id)
        user = User.objects.get(pk=self.request.POST['user'][0])
        user.groups.add(group)  

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


    def form_valid(self, form):

        team = Team.objects.get(pk=self.kwargs['team_id'])
        teamuser = TeamUsers.objects.get(pk=self.kwargs['pk'])

        group = Group.objects.get(pk=team.group_ptr_id)

        user = User.objects.get(pk=teamuser.user_id)
        
        user.groups.remove(group)  

        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['organization_id']}/team/{self.kwargs['team_id']}"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete Team User'

        return context
