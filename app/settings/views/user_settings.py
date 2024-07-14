
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views import generic

from access.mixin import OrganizationPermission

from api.forms.user_token import AuthTokenForm, AuthToken

from core.views.common import AddView, ChangeView, DeleteView

from settings.forms.user_settings import UserSettingsForm
from settings.models.user_settings import UserSettings



class View(ChangeView):

    context_object_name = "settings"

    form_class = UserSettingsForm

    model = UserSettings

    template_name = 'settings/user_settings.html.j2'


    def get_context_data(self, **kwargs):

        if self.object.is_owner(self.request.user):

            context = super().get_context_data(**kwargs)

            context['tokens'] = AuthToken.objects.filter(user=self.kwargs['pk'])

            context['model_docs_path'] = 'user_settings/'

            context['content_title'] = 'User Settings'

            return context
        
        raise PermissionDenied()


    def get_success_url(self, **kwargs):

        return reverse('_settings_user', args=(self.kwargs['pk'],))


class Change(ChangeView):

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


class TokenAdd(AddView):

    context_object_name = "settings"

    form_class = AuthTokenForm

    model = AuthToken

    template_name = 'form.html.j2'


    def form_valid(self, form):

        form.instance.user = self.request.user
        form.instance.token = form.instance.token_hash(form.fields['gen_token'].initial)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):

        if self.request.user.id != self.kwargs['user_id']:

            raise PermissionDenied()

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Generate Authentication Token'

        return context


    def get_success_url(self, **kwargs):

        return reverse('_settings_user', args=(self.kwargs['user_id'],))


class TokenDelete(DeleteView):
    model = AuthToken

    template_name = 'form.html.j2'


    def delete(self, request, *args, **kwargs):

        if self.request.user.id != self.kwargs['user_id']:

            raise PermissionDenied()
            return None

        return super().delete(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        if self.request.user.id != self.kwargs['user_id']:

            raise PermissionDenied()
            return None

        return super().post(request, *args, **kwargs)


    def get_success_url(self, **kwargs):

        return reverse('_settings_user', args=(self.kwargs['user_id'],))


    def get_context_data(self, **kwargs):

        if self.request.user.id != self.kwargs['user_id']:

            raise PermissionDenied()

        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete Token'

        return context

