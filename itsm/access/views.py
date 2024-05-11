from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import TeamForm, TeamsForm
from .models import *


class IndexView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'access.view_organization'
    template_name = 'access/index.html.j2'
    context_object_name = "organization_list"


    def get_queryset(self):

        return Organization.objects.filter()


class OrganizationView(LoginRequiredMixin, generic.DetailView):
    model = Organization
    template_name = "access/organization.html.j2"
    fields = ["team_name", 'id', 'created']


    @method_decorator(permission_required('access.view_organization', raise_exception=True))
    def get(self, request, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        TeamsForm = inlineformset_factory(Organization, Team, fields=["team_name", 'id'], fk_name='organization', extra=1)

        formset = TeamsForm(instance=organization)

        return render(request, self.template_name, {"formset": formset, "organization": organization})


    @method_decorator(permission_required('access.add_organization', raise_exception=True))
    @method_decorator(permission_required('access.edit_organization', raise_exception=True))
    @method_decorator(permission_required('access.delete_organization', raise_exception=True))
    def post(self, request, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        TeamsForm = inlineformset_factory(Organization, Team, fields=["team_name", 'id'], fk_name='organization', extra=1)


        formset = TeamsForm(request.POST, request.FILES, instance=organization)

        if formset.is_valid():

            formset.save()

            # Do something. Should generally end with a redirect. For example:
            # return HttpResponseRedirect(team.get_absolute_url(organization_id))
            return HttpResponseRedirect('#')


        # formset = TeamsForm(instance=organization)

        return render(request, self.template_name, {"formset": formset, "organization": organization})


class TeamView(generic.UpdateView):
    model = Team
    template_name = 'access/team.html.j2'
    user = User

    readonly_fields = ['team_name']


    @method_decorator(permission_required('access.view_team', raise_exception=True))
    def get(self, request, organization_id, team_id):

        team = Team.objects.get(pk=team_id)

        TeamForm = inlineformset_factory(Team, TeamUsers, fields=['id', 'user', 'manager'], fk_name='team', extra=1)

        permissions = Permission.objects.filter()

        formset = TeamForm(instance=team)

        return render(request, self.template_name, {"formset": formset, "team": team, 'permissions': permissions})
        # return render(request, self.template_name)


    @method_decorator(permission_required('access.add_team', raise_exception=True))
    @method_decorator(permission_required('access.change_team', raise_exception=True))
    @method_decorator(permission_required('access.delete_team', raise_exception=True))
    def post(self, request, organization_id, team_id):
        team = Team.objects.get(pk=team_id)
        TeamForm = inlineformset_factory(Team, TeamUsers, fields=['user'], fk_name='team', extra=1)


        formset = TeamForm(request.POST, request.FILES, instance=team)

        if formset.is_valid():

            formset.save()
            # Do something. Should generally end with a redirect. For example:
            # return HttpResponseRedirect(team.get_absolute_url(organization_id, team_id))
            return HttpResponseRedirect('#')


        return render(request, self.template_name, {"formset": formset, "team": team})
