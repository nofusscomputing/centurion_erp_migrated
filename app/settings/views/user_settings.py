
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from settings.forms.user_settings import UserSettingsForm
from settings.models.user_settings import UserSettings



class View(generic.UpdateView):

    context_object_name = "settings"

    form_class = UserSettingsForm

    model = UserSettings

    template_name = 'settings/user_settings.html.j2'


    def get_context_data(self, **kwargs):

        if self.object.is_owner(self.request.user):

            context = super().get_context_data(**kwargs)

            context['content_title'] = 'User Settings'

            return context
        
        raise PermissionDenied()



class Change(generic.UpdateView):

    context_object_name = "settings"

    form_class = UserSettingsForm

    model = UserSettings

    template_name = 'form.html.j2'


    def form_valid(self, form):

        if self.object.is_owner(self.request.user):

            return super().form_valid(form)

        raise PermissionDenied()


    def get_success_url(self, **kwargs):

        return reverse('_settings_user', args=(self.kwargs['pk'],))


    def get_context_data(self, **kwargs):

        if self.object.is_owner(self.request.user):

            context = super().get_context_data(**kwargs)

            context['content_title'] = 'User Settings'

            return context
        
        raise PermissionDenied()
