from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic

from access.forms import TeamForm
from access.models import *
from access.mixin import *



class IndexView(PermissionRequiredMixin, OrganizationPermission, generic.ListView):
    permission_required = 'access.view_organization'
    template_name = 'access/index.html.j2'
    context_object_name = "organization_list"


    def get_queryset(self):

        if self.request.user.is_superuser:

            return Organization.objects.filter()

        else:

            return Organization.objects.filter(pk__in=self.user_organizations())



class OrganizationView(LoginRequiredMixin, OrganizationPermission, generic.UpdateView):
    model = Organization
    permission_required = 'access.view_organization'
    template_name = "access/organization.html.j2"
    fields = ["name", 'id']


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"

    def get_queryset(self):

        return Organization.objects.filter(pk=self.kwargs['pk'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organization = Organization.objects.get(pk=self.kwargs['pk'])

        context['organization'] = organization

        TeamsForm = inlineformset_factory(Organization, Team, fields=["team_name", 'id'], fk_name='organization', extra=1)
        formset = TeamsForm(instance=organization)

        context['formset'] = formset

        return context



class OrganizationChange(LoginRequiredMixin, OrganizationPermission, generic.DetailView):
    pass



class OrganizationDelete(LoginRequiredMixin, OrganizationPermission, generic.DetailView):
    pass










class TeamView(OrganizationPermission, generic.UpdateView):
    model = Team
    permission_required = 'access.view_team'
    template_name = 'access/team.html.j2'
    user = User

    readonly_fields = ['team_name']


    def get(self, request, organization_id, pk):

        team = Team.objects.get(pk=pk)

        TeamForm = inlineformset_factory(Team, TeamUsers, fields=['id', 'user', 'manager'], fk_name='team', extra=1)

        permissions = Permission.objects.filter()

        formset = TeamForm(instance=team)

        return render(request, self.template_name, {"formset": formset, "team": team, 'organization_id': organization_id, 'permissions': permissions})


    def post(self, request, organization_id, pk):
        team = Team.objects.get(pk=pk)
        TeamForm = inlineformset_factory(Team, TeamUsers, fields=['user'], fk_name='team', extra=1)


        formset = TeamForm(request.POST, request.FILES, instance=team)

        if formset.is_valid():

            formset.save()

            return HttpResponseRedirect('#')


        return render(request, self.template_name, {"formset": formset, 'organization_id': organization_id, "team_id": pk, "team": team})


class TeamAdd(OrganizationPermission, generic.CreateView):
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


class TeamChange(OrganizationPermission, generic.UpdateView):
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



class TeamDelete(OrganizationPermission, generic.DeleteView):
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
