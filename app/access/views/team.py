from django.contrib.auth import decorators as auth_decorator
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic

from access.models import Team, TeamUsers, Organization
from access.mixin import *



class View(OrganizationPermission, generic.UpdateView):
    model = Team
    permission_required = [
        'access.view_team',
        'access.change_team',
    ]
    template_name = 'access/team.html.j2'

    fields = [
        "name",
        'id',
        'organization',
        'permissions'
    ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organization = Organization.objects.get(pk=self.kwargs['organization_id'])

        context['organization'] = organization

        team = Team.objects.get(pk=self.kwargs['pk'])

        teamusers = TeamUsers.objects.filter(team=self.kwargs['pk'])

        context['teamusers'] = teamusers
        context['permissions'] = Permission.objects.filter()

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        return context

    def get_success_url(self, **kwargs):
        return reverse('Access:_team_view', args=(self.kwargs['organization_id'], self.kwargs['pk'],))


    @method_decorator(auth_decorator.permission_required("access.change_team", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(OrganizationPermission, generic.CreateView):
    model = Team
    permission_required = [
        'access.add_team',
    ]
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

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['content_title'] = 'Add Team'

        return context



class Delete(OrganizationPermission, generic.DeleteView):
    model = Team
    permission_required = [
        'access.delete_team'
    ]
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

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['content_title'] = 'Delete Team'

        return context














