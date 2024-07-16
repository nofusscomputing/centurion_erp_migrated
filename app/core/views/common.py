from django.views import generic

from access.mixin import OrganizationPermission

from core.exceptions import MissingAttribute

from settings.models.user_settings import UserSettings



class View(OrganizationPermission):
    """ Abstract class common to all views

    !!! Danger
        Don't directly use this class within your view as it's already assigned to the views that require it.
    """

    template_name:str  = 'form.html.j2'


    def get_form_kwargs(self) -> dict:
        """ Fetch kwargs for form

        Returns:
            dict: kwargs used in fetching form
        """

        kwargs = super().get_form_kwargs()

        if self.form_class:

            kwargs.update({'user': self.request.user})

        return kwargs



class AddView(View, generic.CreateView):

    template_name:str  = 'form.html.j2'

    def get_initial(self):

        return {
            'organization': UserSettings.objects.get(user = self.request.user).default_organization
        }


class ChangeView(View, generic.UpdateView):

    template_name:str  = 'form.html.j2'



class DeleteView(OrganizationPermission, generic.DeleteView):

    template_name:str  = 'form.html.j2'



class DisplayView(OrganizationPermission, generic.DetailView):
    """ A View used for displaying arbitrary data """

    template_name:str  = 'form.html.j2'



class IndexView(View, generic.ListView):

    model = None
    """ Model the view is for

    Leaving this value unset will prevent the item from showing up within the navigation menu
    """

    template_name:str = None

    def __init__(self, **kwargs):

        if not self.model:

            raise MissingAttribute('Model is required for view')

        super().__init__(**kwargs)
