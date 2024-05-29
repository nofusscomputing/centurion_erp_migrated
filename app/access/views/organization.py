from django.contrib.auth import decorators as auth_decorator
from django.utils.decorators import method_decorator
from django.views import generic

from access.mixin import *
from access.models import *



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
    model = Organization
    permission_required = [
        'access.view_organization',
        'access.change_organization',
    ]
    template_name = "access/organization.html.j2"
    fields = ["name", 'id']


    def get_success_url(self, **kwargs):
        return f"/organization/{self.kwargs['pk']}/"

    def get_queryset(self):

        return Organization.objects.filter(pk=self.kwargs['pk'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['organization'] = Organization.objects.get(pk=self.kwargs['pk'])

        context['teams'] = Team.objects.filter(organization=self.kwargs['pk'])

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        return context


    @method_decorator(auth_decorator.permission_required("access.change_organization", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Change(OrganizationPermission, generic.DetailView):
    pass



class Delete(OrganizationPermission, generic.DetailView):
    pass









