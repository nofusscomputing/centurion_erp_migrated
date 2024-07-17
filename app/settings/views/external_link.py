from django.contrib.auth import decorators as auth_decorator
from django.db.models import Q
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic


from access.mixin import OrganizationPermission

from core.views.common import AddView, ChangeView, DeleteView, DisplayView, IndexView

from settings.forms.external_links import ExternalLinksForm
from settings.models.external_link import ExternalLink


class Index(IndexView):

    context_object_name = "list"

    model = ExternalLink

    paginate_by = 10

    permission_required = [
        'settings.view_externallink'
    ]

    template_name = 'settings/external_links.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_docs_path'] = self.model._meta.app_label + '/external_links/'

        context['content_title'] = 'External Links'

        return context




class View(ChangeView):

    context_object_name = "externallink"

    form_class = ExternalLinksForm

    model = ExternalLink

    permission_required = [
        'settings.view_externallink',
    ]

    template_name = 'settings/external_link.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_pk'] = self.kwargs['pk']
        context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

        context['model_delete_url'] = reverse('Settings:_external_link_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_external_link_view', args={self.kwargs['pk']})


    @method_decorator(auth_decorator.permission_required("settings.change_externallink", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)


class Change(ChangeView):

    context_object_name = "externallink"

    form_class = ExternalLinksForm

    model = ExternalLink

    permission_required = [
        'settings.change_externallink',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['content_title'] = self.object.name

        return context

    def get_success_url(self, **kwargs):

        return reverse('Settings:_external_link_view', args={self.kwargs['pk']})


    @method_decorator(auth_decorator.permission_required("settings.change_externallink", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(AddView):

    
    form_class = ExternalLinksForm

    model = ExternalLink

    permission_required = [
        'settings.add_externallink',
    ]

    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse(viewname = 'Settings:External Links')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add External Link'

        return context


class Delete(DeleteView):

    model = ExternalLink

    permission_required = [
        'settings.delete_externallink',
    ]

    template_name = 'form.html.j2'

    def get_success_url(self, **kwargs):

        return reverse('Settings:External Links')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context

