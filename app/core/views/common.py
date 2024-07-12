from django.views import generic

from access.mixin import OrganizationPermission



class View(OrganizationPermission):
    """ Abstract class common to all views

    !!! Danger
        Don't directly use this class within your view as it's already assigned to the views that require it.
    """


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

    pass



class ChangeView(View, generic.UpdateView):

    pass



class DeleteView(OrganizationPermission, generic.DeleteView):

    pass


class DisplayView(OrganizationPermission, generic.DetailView):
    """ A View used for displaying arbitrary data """

    pass



class IndexView(View, generic.ListView):

    model = None
    """ Model the view is for

    Leaving this value unset will prevent the item from showing up within the navigation menu
    """

    def __init__(self, **kwargs):

        if not self.model:

            raise Exception('Model is required for view')

        super().__init__(**kwargs)
