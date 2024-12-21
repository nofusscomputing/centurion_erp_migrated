from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from assistance.serializers.request import TicketBaseSerializer

from core.fields.badge import BadgeField
from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_linked_items import TicketLinkedItem



class TicketLinkedItemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return item.get_url( request = self._context['view'].request )


    created = serializers.DateTimeField( source = 'ticket.created', read_only = True )

    class Meta:

        model = TicketLinkedItem

        fields = [
            'id',
            'display_name',
            'created'
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created'
            'url',
        ]


class TicketLinkedItemModelSerializer(
    TicketLinkedItemBaseSerializer,
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request )
        }


    class Meta:

        model = TicketLinkedItem

        fields = [
            'id',
            'display_name',
            'item',
            'item_type',
            'ticket',
            'organization',
            'created',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'organization',
            'created',
            '_urls',
        ]


    def get_field_names(self, declared_fields, info):

        if 'view' in self._context:

            if(
                'item_class' in self.context['view'].kwargs
                and 'item_id' in self.context['view'].kwargs
            ):

                self.Meta.read_only_fields += [ 'item', 'item_type' ]

        fields = super().get_field_names(declared_fields, info)

        return fields


    def validate(self, data):

        ticket = None

        if 'view' in self._context:

            if 'ticket_id' in self._context['view'].kwargs:

                ticket = Ticket.objects.get(pk = int(self._context['view'].kwargs['ticket_id']) )

            if 'item_class' in self._context['view'].kwargs:

                data['item_type'] = self._context['view'].item_type


            if 'item_id' in self._context['view'].kwargs:

                data['item'] = int(self._context['view'].kwargs['item_id'])


        if (
            'ticket' in data
            and ticket is None
        ):

            ticket = data['ticket']


        if ticket:

            data['ticket'] = ticket

            data['organization_id'] = ticket.organization.id

        else:

            raise serializers.ValidationError(
                detail = {
                    'ticket': 'Ticket is required'
                },
                code = 'required'
            )


        return data



class TicketLinkedItemViewSerializer(TicketLinkedItemModelSerializer):


    organization = OrganizationBaseSerializer(many=False, read_only=True)

    item = serializers.SerializerMethodField('get_item')

    def get_item(self, item) -> dict:

        base_serializer: dict = None

        if item.item_type == TicketLinkedItem.Modules.CLUSTER:

            from itim.serializers.cluster import Cluster, ClusterBaseSerializer

            base_serializer = ClusterBaseSerializer

            model = Cluster

        elif item.item_type == TicketLinkedItem.Modules.CONFIG_GROUP:

            from config_management.serializers.config_group import ConfigGroups, ConfigGroupBaseSerializer

            base_serializer = ConfigGroupBaseSerializer

            model = ConfigGroups

        elif item.item_type == TicketLinkedItem.Modules.DEVICE:

            from itam.serializers.device import Device, DeviceBaseSerializer

            base_serializer = DeviceBaseSerializer

            model = Device

        elif item.item_type == TicketLinkedItem.Modules.KB:

            from assistance.serializers.knowledge_base import KnowledgeBase, KnowledgeBaseBaseSerializer

            base_serializer = KnowledgeBaseBaseSerializer

            model = KnowledgeBase

        elif item.item_type == TicketLinkedItem.Modules.OPERATING_SYSTEM:

            from itam.serializers.operating_system import OperatingSystem, OperatingSystemBaseSerializer

            base_serializer = OperatingSystemBaseSerializer

            model = OperatingSystem

        elif item.item_type == TicketLinkedItem.Modules.ORGANIZATION:

            from access.serializers.organization import Organization, OrganizationBaseSerializer

            base_serializer = OrganizationBaseSerializer

            model = Organization

        elif item.item_type == TicketLinkedItem.Modules.SERVICE:

            from itim.serializers.service import Service, ServiceBaseSerializer

            base_serializer = ServiceBaseSerializer

            model = Service

        elif item.item_type == TicketLinkedItem.Modules.SOFTWARE:

            from itam.serializers.software import Software, SoftwareBaseSerializer

            base_serializer = SoftwareBaseSerializer

            model = Software

        elif item.item_type == TicketLinkedItem.Modules.TEAM:

            from access.serializers.teams import Team, TeamBaseSerializer

            base_serializer = TeamBaseSerializer

            model = Team

        
        if not base_serializer:

            return {
                'id': int(item.item)
            }

        
        try:

            model = model.objects.get(
                pk = int(item.item) 
            )

        except:

            return {}


        return base_serializer(
            model,
            context=self._context
        ).data

    ticket = TicketBaseSerializer(read_only = True)
