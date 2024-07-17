from django.template import Template, Context
from django.utils.html import escape
from django.views import generic

from access.mixin import OrganizationPermission

from core.exceptions import MissingAttribute

from settings.models.external_link import ExternalLink
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

    # ToDo: on migrating all views to seperate display and change views, external_links will not be required in `ChangView`
    def get_context_data(self, **kwargs):
        """ Get template context

        For items that have the ability to have external links, this function
        adds the external link details to the context.

        !!! Danger "Requirement"
            This function may be overridden with the caveat that this function is still called.
            by the overriding function. i.e. `super().get_context_data(skwargs)`

        !!! note
            The adding of `external_links` within this view is scheduled to be removed.

        Returns:
            (dict): Context for the template to use inclusive of 'external_links'
        """

        context = super().get_context_data(**kwargs)

        external_links_query = None


        if self.model._meta.model_name == 'device':

            external_links_query = ExternalLink.objects.filter(devices=True)

        elif self.model._meta.model_name == 'software':

            external_links_query = ExternalLink.objects.filter(software=True)


        if external_links_query:

            external_links: list = []

            user_context = Context(context)

            for external_link in external_links_query:

                user_string = Template(external_link)
                external_link_context: dict = {
                        'name': escape(external_link.name),
                        'link': escape(user_string.render(user_context)),
                    }

                if external_link.colour:

                    external_link_context.update({'colour': external_link.colour })
                external_links += [ external_link_context ]

            context['external_links'] = external_links


        return context


class DeleteView(OrganizationPermission, generic.DeleteView):

    template_name:str  = 'form.html.j2'



class DisplayView(OrganizationPermission, generic.DetailView):
    """ A View used for displaying arbitrary data """

    template_name:str  = 'form.html.j2'


    # ToDo: on migrating all views to seperate display and change views, external_links will not be required in `ChangView`
    def get_context_data(self, **kwargs):
        """ Get template context

        For items that have the ability to have external links, this function
        adds the external link details to the context.

        !!! Danger "Requirement"
            This function may be overridden with the caveat that this function is still called.
            by the overriding function. i.e. `super().get_context_data(skwargs)`

        Returns:
            (dict): Context for the template to use inclusive of 'external_links'
        """

        context = super().get_context_data(**kwargs)

        external_links_query = None


        if self.model._meta.model_name == 'device':

            external_links_query = ExternalLink.objects.filter(devices=True)

        elif self.model._meta.model_name == 'software':

            external_links_query = ExternalLink.objects.filter(software=True)


        if external_links_query:

            external_links: list = []

            user_context = Context(context)

            for external_link in external_links_query:

                user_string = Template(external_link)
                external_link_context: dict = {
                        'name': escape(external_link.name),
                        'link': escape(user_string.render(user_context)),
                    }

                if external_link.colour:

                    external_link_context.update({'colour': external_link.colour })
                external_links += [ external_link_context ]

            context['external_links'] = external_links


        return context



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
