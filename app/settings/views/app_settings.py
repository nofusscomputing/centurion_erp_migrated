
from django.core.exceptions import EmptyResultSet, PermissionDenied, ValidationError
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from core.views.common import ChangeView

from settings.forms.app_settings import AppSettingsForm
from settings.models.app_settings import AppSettings



class View(generic.UpdateView):

    context_object_name = "settings"

    form_class = AppSettingsForm

    model = AppSettings

    permission_required = [
        'settings.change_appsettings'
    ]

    template_name = 'form.html.j2'


    def get_object(self, queryset=None):

        obj = self.model.objects.get(owner_organization=None)

        if obj:

            return obj

        raise EmptyResultSet('No Application Settings found')


    def form_valid(self, form):

        form.instance.id = self.object.pk

        if self.request.user.is_superuser:

            return super().form_valid(form)

        raise PermissionDenied()


    def get_success_url(self, **kwargs):

        return reverse('Settings:_settings_application')


    def get_context_data(self, **kwargs):

        if self.request.user.is_superuser:

            context = super().get_context_data(**kwargs)

            context['model_docs_path'] = self.model._meta.app_label + '/'
            context['model_pk'] = self.object.pk
            context['model_name'] = self.model._meta.verbose_name.replace(' ', '')

            context['content_title'] = 'Application Settings'

            return context
        
        raise PermissionDenied()
