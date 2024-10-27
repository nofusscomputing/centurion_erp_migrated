from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from api.exceptions import UnknownTicketType

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_comment import Ticket, TicketComment



class TicketCommentBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = TicketComment

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]



class TicketCommentModelSerializer(TicketCommentBaseSerializer):
    """Base class for Ticket Comment Model

    Args:
        TicketCommentBaseSerializer (class): Base class for ALL commment types.

    Raises:
        UnknownTicketType: Ticket type is undetermined.
    """

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        request = self.context.get('request')

        if item.ticket:

            ticket_type_name = item.ticket.get_ticket_type_display()

            ticket_id = item.ticket.id

        else:

            raise UnknownTicketType()


        urls: dict = {
            '_self': reverse(
                    'API:_api_v2_ticket_' + str(ticket_type_name).lower().replace(' ', '_') + '_comments-detail',
                    request = self._context['view'].request,
                    kwargs={
                        'ticket_id': ticket_id,
                        'pk': item.id
                    }
                )
        }

        threads = TicketComment.objects.filter(parent = item.id, ticket = ticket_id)

        if len(threads) > 0:

            urls.update({
                'threads': reverse(
                    'API:_api_v2_ticket_' + str(ticket_type_name).lower().replace(' ', '_') + '_comment_threads-list',
                    request = self._context['view'].request,
                    kwargs={
                        'ticket_id': ticket_id,
                        'parent_id': item.id
                    }
                )
            })

        return urls


    class Meta:

        model = TicketComment

        fields = '__all__'

        fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'body',
            'private',
            'duration',
            'category',
            'template',
            'is_template',
            'source',
            'status',
            'responsible_user',
            'responsible_team',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'private',
            'duration',
            'category',
            'template',
            'is_template',
            'source',
            'status',
            'responsible_user',
            'responsible_team',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]


   
    def __init__(self, instance=None, data=empty, **kwargs):

        if 'context' in self._kwargs:

            if 'view' in self._kwargs['context']:

                if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                    ticket = Ticket.objects.get(pk=int(self._kwargs['context']['view'].kwargs['ticket_id']))
                    self.fields.fields['organization'].initial = ticket.organization.id

                    self.fields.fields['ticket'].initial = ticket.id

                    self.fields.fields['comment_type'].initial = TicketComment.CommentType.COMMENT

                    self.fields.fields['user'].initial = kwargs['context']['request']._user.id

        super().__init__(instance=instance, data=data, **kwargs)



class TicketCommentITILModelSerializer(TicketCommentModelSerializer):
    """ITIL Comment Model Base

    This serializer is the base for ALL ITIL comment Types.

    Args:
        TicketCommentModelSerializer (class): Base comment class for ALL comments
    """

    class Meta(TicketCommentModelSerializer.Meta):

        fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'body',
            'private',
            'duration',
            'category',
            'template',
            'is_template',
            'source',
            'status',
            'responsible_user',
            'responsible_team',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'body',
            'private',
            'duration',
            'category',
            'template',
            'is_template',
            'source',
            'status',
            'responsible_user',
            'responsible_team',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]



class TicketCommentITILFollowUpModelSerializer(TicketCommentITILModelSerializer):
    """ITIL Followup Comment

    Args:
        TicketCommentITILModelSerializer (class): Base class for ALL ITIL comment types.
    """

    class Meta(TicketCommentITILModelSerializer.Meta):

        read_only_fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            # 'body',
            'private',
            'duration',
            # 'category',
            # 'template',
            'is_template',
            # 'source',
            'status',
            # 'responsible_user',
            # 'responsible_team',
            'user',
            # 'planned_start_date',
            # 'planned_finish_date',
            # # 'real_start_date',
            # 'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]



class TicketCommentITILTaskModelSerializer(TicketCommentITILModelSerializer):
    """ITIL Task Comment

    Args:
        TicketCommentITILModelSerializer (class): Base class for ALL ITIL comment types.
    """

    class Meta(TicketCommentITILModelSerializer.Meta):

        read_only_fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            # 'body',
            'private',
            'duration',
            # 'category',
            # 'template',
            'is_template',
            'source',
            'status',
            # 'responsible_user',
            # 'responsible_team',
            'user',
            # 'planned_start_date',
            # 'planned_finish_date',
            # 'real_start_date',
            # 'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]



class TicketCommentITILSolutionModelSerializer(TicketCommentITILModelSerializer):
    """ITIL Solution Comment

    Args:
        TicketCommentITILModelSerializer (class): Base class for ALL ITIL comment types.
    """

    class Meta(TicketCommentITILModelSerializer.Meta):

        read_only_fields = [
            'id',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'private',
            'duration',
            'is_template',
            'source',
            'status',
            'responsible_user',
            'responsible_team',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'organization',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]



class TicketCommentImportModelSerializer(TicketCommentModelSerializer):
    """Import User Serializer

    Args:
        TicketCommentModelSerializer (class): Base class for ALL comment types.
    """

    class Meta(TicketCommentModelSerializer.Meta):

        read_only_fields = [
            'id',
            # 'parent',
            # 'ticket',
            # 'external_ref',
            # 'external_system',
            # 'comment_type',
            # 'body',
            # 'private',
            'duration',
            # 'category',
            # 'template',
            # 'is_template',
            # 'source',
            # 'status',
            # 'responsible_user',
            # 'responsible_team',
            # 'user',
            # 'planned_start_date',
            # 'planned_finish_date',
            # 'real_start_date',
            # 'real_finish_date',
            # 'organization',
            # 'date_closed',
            # 'created',
            # 'modified',
            '_urls',
        ]



class TicketCommentViewSerializer(TicketCommentModelSerializer):

    organization = OrganizationBaseSerializer( many = False, read_only = True ) 

    user = UserBaseSerializer()

    responsible_user = UserBaseSerializer()

    responsible_team = TeamBaseSerializer()
