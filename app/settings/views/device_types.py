from django.db.models import Q
from django.views import generic


from access.mixin import OrganizationPermission
from itam.models.device import DeviceType



class Index(OrganizationPermission, generic.ListView):
    model = DeviceType

    permission_required = 'itam.view_devicetype'

    template_name = 'settings/device_types.html.j2'

    context_object_name = "list"

    paginate_by = 10


    def get_queryset(self):

        if self.request.user.is_superuser:

            return self.model.objects.filter().order_by('name')

        else:

            return self.model.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True)).order_by('name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Device Types'

        return context
