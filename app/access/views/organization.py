from django.contrib.auth import decorators as auth_decorator
from django.utils.decorators import method_decorator
from django.views import generic

from access.mixin import *
from access.models import *

from access.forms.organization import OrganizationForm



class IndexView(OrganizationPermission, generic.ListView):
    permission_required = [
        'access.view_organization'
    ]
    template_name = 'access/index.html.j2'
    context_object_name = "organization_list"


    def get_queryset(self):

        if self.request.user.is_superuser:

            return Organization.objects.filter()

        else:

            return Organization.objects.filter(pk__in=self.user_organizations())



class View(OrganizationPermission, generic.UpdateView):

    context_object_name = "organization"

    form_class = OrganizationForm

    model = Organization

    template_name = "access/organization.html.j2"

    def get(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:

                return self.handle_no_permission()

        if not self.permission_check(request, [ 'access.view_organization' ]):

            raise PermissionDenied('You are not part of this organization')

        return super().get(request, *args, **kwargs)


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"

    def get_queryset(self):

        return Organization.objects.filter(pk=self.kwargs['pk'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/' + self.model._meta.model_name + '/'

        context['teams'] = Team.objects.filter(organization=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        return context


    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

                return self.handle_no_permission()

        if not self.permission_check(request, [ 'access.change_organization' ]):

            raise PermissionDenied('You are not part of this organization')

        return super().post(request, *args, **kwargs)



class Change(OrganizationPermission, generic.DetailView):
    pass



class Delete(OrganizationPermission, generic.DetailView):
    pass









