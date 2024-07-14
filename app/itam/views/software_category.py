from django.contrib.auth import decorators as auth_decorator
from django.urls import reverse
from django.utils.decorators import method_decorator

from core.views.common import AddView, ChangeView, DeleteView

from itam.forms.software_category import SoftwareCategoryForm
from itam.models.software import Software, SoftwareCategory

from settings.models.user_settings import UserSettings


class View(ChangeView):

    context_object_name = "software"

    form_class = SoftwareCategoryForm

    model = SoftwareCategory

    permission_required = [
        'itam.view_softwarecategory',
        'itam.change_softwarecategory',
    ]

    template_name = 'form.html.j2'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_delete_url'] = reverse('Settings:_software_category_delete', args=(self.kwargs['pk'],))

        context['content_title'] = self.object.name

        return context


    def get_success_url(self, **kwargs):

        return reverse('Settings:_software_category_view', args=(self.kwargs['pk'],))


    @method_decorator(auth_decorator.permission_required("itam.change_softwarecategory", raise_exception=True))
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)



class Add(AddView):

    form_class = SoftwareCategoryForm

    model = SoftwareCategory

    permission_required = [
        'itam.add_softwarecategory',
    ]

    template_name = 'form.html.j2'

    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


    def get_success_url(self, **kwargs):

        return reverse('Settings:_software_categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Add Software Category'

        return context



class Delete(DeleteView):
    model = SoftwareCategory
    permission_required = [
        'itam.delete_softwarecategory',
    ]
    template_name = 'form.html.j2'


    def get_success_url(self, **kwargs):

        return reverse('Settings:_software_categories')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Delete ' + self.object.name

        return context
