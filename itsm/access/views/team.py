from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.views import generic

from access.forms import TeamForm
from access.models import Team, TeamUsers, Organization
from access.mixin import *



class View(OrganizationPermission, generic.UpdateView):
    model = Team
    permission_required = 'access.view_team'
    template_name = 'access/team.html.j2'

    fields = [
        "name",
        'id'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organization = Organization.objects.get(pk=self.kwargs['organization_id'])

        context['organization'] = organization

        team = Team.objects.get(pk=self.kwargs['pk'])

        teamusers = TeamUsers.objects.filter(team=self.kwargs['pk'])

        context['teamusers'] = teamusers
        context['permissions'] = permissions = Permission.objects.filter()

        return context

    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['organization_id']}/team/{self.kwargs['pk']}/"



class Add(PermissionRequiredMixin, OrganizationPermission, generic.CreateView):
    model = Team
    permission_required = 'access.add_team'
    template_name = 'form.html.j2'
    fields = [
        'team_name',
    ]

    def form_valid(self, form):
        form.instance.organization = Organization.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Team'

        return context


class Change(PermissionRequiredMixin, OrganizationPermission, generic.UpdateView):
    model = Team
    permission_required = 'access.change_team'
    template_name = 'form.html.j2'
    fields = [
        'team_name',
        'permissions',
        'organization'
    ]

    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Edit Team'

        return context



class Delete(PermissionRequiredMixin, OrganizationPermission, generic.DeleteView):
    model = Team
    permission_required = 'access.delete_team'
    template_name = 'form.html.j2'
    fields = [
        'team_name',
        'permissions',
        'organization'
    ]


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['organization_id']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete Team'

        return context














