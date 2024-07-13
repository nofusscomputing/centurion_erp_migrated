from django.contrib.auth import decorators as auth_decorator
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.urls import reverse

from access.forms.team import TeamForm, TeamFormAdd
from access.models import Team, TeamUsers, Organization
from access.mixin import *

from core.views.common import AddView, ChangeView, DeleteView


class View(ChangeView):

    context_object_name = "team"

    form_class = TeamForm

    model = Team

    permission_required = [
        'access.view_team',
        'access.change_team',
    ]

    template_name = 'access/team.html.j2'


    def get(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:

                return self.handle_no_permission()

        if not self.permission_check(request, [ 'access.view_team' ]):

            raise PermissionDenied('You are not part of this organization')

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'


        organization = Organization.objects.get(pk=self.kwargs['organization_id'])

        context['organization'] = organization

        team = Team.objects.get(pk=self.kwargs['pk'])

        teamusers = TeamUsers.objects.filter(team=self.kwargs['pk'])

        context['teamusers'] = teamusers

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        return context

    def get_success_url(self, **kwargs):
        return reverse('Access:_team_view', args=(self.kwargs['organization_id'], self.kwargs['pk'],))


    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

                return self.handle_no_permission()

        if not self.permission_check(request, [ 'access.change_team' ]):

            raise PermissionDenied('You are not part of this organization')

        return super().post(request, *args, **kwargs)



class Add(AddView):

    form_class = TeamFormAdd

    model = Team

    parent_model = Organization

    permission_required = [
        'access.add_team',
    ]

    template_name = 'form.html.j2'

    def form_valid(self, form):
        form.instance.organization = Organization.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['content_title'] = 'Add Team'

        return context



class Delete(DeleteView):
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














