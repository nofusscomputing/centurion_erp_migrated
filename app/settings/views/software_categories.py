from access.mixin import OrganizationPermission

from core.views.common import IndexView

from itam.models.software import SoftwareCategory


class Index(IndexView):

    model = SoftwareCategory

    permission_required = [
        'itam.view_software'
    ]

    template_name = 'settings/software_categories.html.j2'

    context_object_name = "list"

    paginate_by = 10


    def get_queryset(self):

        return self.model.objects.filter().order_by('name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Software Categories'

        return context
