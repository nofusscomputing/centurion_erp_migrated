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

        kwargs.update({'user': self.request.user})

        return kwargs



class AddView(View, generic.CreateView):

    pass



class ChangeView(View, generic.UpdateView):

    pass



class DeleteView(generic.DeleteView):

    pass



class IndexView(View, generic.ListView):

    pass
