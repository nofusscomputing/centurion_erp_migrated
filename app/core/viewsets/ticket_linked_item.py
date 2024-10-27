from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.ticket_linked_item import (
    TicketLinkedItem,
    TicketLinkedItemModelSerializer,
    TicketLinkedItemViewSerializer
)

from api.views.mixin import OrganizationPermissionAPI

from api.viewsets.common import ModelViewSet


@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Ticket Linked Item',
        description='',
        responses = {
            201: OpenApiResponse(description='Created', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Ticket Linked Item',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Ticket Linked Items',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Ticket Linked Item',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Ticket Linked Item',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'item_type',
        'organization',
    ]

    search_fields = []

    model = TicketLinkedItem

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']


    def get_queryset(self):

        if 'ticket_id' in self.kwargs:

            self.queryset = TicketLinkedItem.objects.filter(ticket=self.kwargs['ticket_id']).order_by('id')

        elif 'item_id' in self.kwargs:

            item_type: int = None

            for choice in list(map(lambda c: c.name, TicketLinkedItem.Modules)):

                if str(getattr(TicketLinkedItem.Modules, 'CLUSTER').label).lower() == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'CLUSTER').value

                elif str(getattr(TicketLinkedItem.Modules, 'CONFIG_GROUP').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'CONFIG_GROUP').value

                elif str(getattr(TicketLinkedItem.Modules, 'DEVICE').label).lower() == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'DEVICE').value

                elif str(getattr(TicketLinkedItem.Modules, 'OPERATING_SYSTEM').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'OPERATING_SYSTEM').value

                elif str(getattr(TicketLinkedItem.Modules, 'SERVICE').label).lower() == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'SERVICE').value

                elif str(getattr(TicketLinkedItem.Modules, 'SOFTWARE').label).lower() == self.kwargs['item_class']:

                    item_type = getattr(TicketLinkedItem.Modules, 'SOFTWARE').value

            self.queryset = TicketLinkedItem.objects.filter(
                item=int(self.kwargs['item_id']),
                item_type = item_type
            )

        if 'pk' in self.kwargs:

            self.queryset = self.queryset.filter(pk = self.kwargs['pk'])

        return self.queryset
