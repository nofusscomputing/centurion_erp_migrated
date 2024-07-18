from core.views.common import IndexView

from itam.models.device import DeviceType



class Index(IndexView):

    model = DeviceType

    permission_required = [
        'itam.view_devicetype'
    ]

    template_name = 'settings/device_types.html.j2'

    context_object_name = "list"

    paginate_by = 10


    def get_queryset(self):

        return self.model.objects.filter().order_by('name')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['content_title'] = 'Device Types'

        return context
