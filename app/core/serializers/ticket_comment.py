from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from access.serializers.organization import Organization, OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from api.exceptions import UnknownTicketType

from app.serializers.user import UserBaseSerializer

from core import exceptions as centurion_exceptions
from core import fields as centurion_field
from core.models.ticket.ticket_comment import Ticket, TicketComment



class TicketCommentBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_ticket_comment-detail", format="html"
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



class TicketCommentModelSerializer(
    TicketCommentBaseSerializer,
):
    """Base class for Ticket Comment Model

    Args:
        TicketCommentBaseSerializer (class): Base class for ALL commment types.

    Raises:
        UnknownTicketType: Ticket type is undetermined.
    """

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        request = self.context.get('request')

        if item.ticket:

            ticket_type_name = item.ticket.get_ticket_type_display()

            ticket_id = item.ticket.id

        else:

            raise UnknownTicketType()


        urls: dict = {
            '_self': reverse(
                    'API:_api_v2_ticket_comment-detail',
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
                    'API:_api_v2_ticket_comment_threads-list',
                    request = self._context['view'].request,
                    kwargs={
                        'ticket_id': ticket_id,
                        'parent_id': item.id
                    }
                )
            })

        return urls


    body = centurion_field.MarkdownField( required = True )


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
            'external_ref',
            'external_system',
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

    is_triage: bool = False
    """ If the serializers is a Triage serializer"""

    request = None
    """ HTTP Request that wwas made"""


    def __init__(self, instance=None, data=empty, **kwargs):

        if data != empty:

            if 'view' in kwargs['context']:

                if kwargs['context']['view'].action == 'create':

                    if(
                        'ticket_id' in kwargs['context']['view'].kwargs
                        and not data['organization']
                    ):

                        data['organization'] = Ticket.objects.get(
                            pk = int(self._kwargs['context']['view'].kwargs['ticket_id'])
                        ).organization.id


        super().__init__(instance=instance, data=data, **kwargs)

        if 'context' in kwargs:

            if 'request' in kwargs['context']:

                self.request = kwargs['context']['request']

            if 'view' in kwargs['context']:

                if kwargs['context']['view'].action == 'create':


                    if 'request' in kwargs['context']['view'].kwargs:

                        self.fields.fields['user'].initial = self.request._user.id



    def validate(self, attrs):

        if(
            (
                'comment_type' not in attrs
                or attrs['comment_type'] is None
            )
            and self._context['view'].action == 'create'
        ):

            raise centurion_exceptions.ValidationError(
                detail = {
                    'comment_type': 'Comment Type is required'
                },
                code = 'required'
            )

        elif (
            'comment_type' in attrs
            and (
                self._context['view'].action == 'partial_update'
                or self._context['view'].action == 'update'
            )
        ):

            raise centurion_exceptions.ValidationError(
                detail = {
                    'comment_type': 'Comment Type is not editable'
                },
                code = 'read_only'
            )

        if self.is_triage:

            attrs = self.validate_triage(attrs)


        return attrs




    def is_valid(self, *, raise_exception=False):

        is_valid: bool = False

        is_valid = super().is_valid(raise_exception=raise_exception)


        if 'view' in self._context:

            if self._context['view'].action == 'create':

                if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                    self.validated_data['ticket_id'] = int(self._kwargs['context']['view'].kwargs['ticket_id'])

                else:

                    raise centurion_exceptions.ValidationError(
                        detail = {
                            'ticket': 'Ticket is a required field'
                        },
                        code = 'required'
                    )

                

        return is_valid



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



class TicketCommentITILFollowUpAddModelSerializer(TicketCommentITILModelSerializer):
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



class TicketCommentITILFollowUpChangeModelSerializer(TicketCommentITILFollowUpAddModelSerializer):

    pass



class TicketCommentITILFollowUpTriageModelSerializer(TicketCommentITILModelSerializer):
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
            # 'private',
            'duration',
            # 'category',
            # 'template',
            # 'is_template',
            # 'source',
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

    is_triage: bool = True

    def validate_triage(self, attrs):

        return attrs


class TicketCommentITILSolutionAddModelSerializer(TicketCommentITILModelSerializer):
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



class TicketCommentITILSolutionChangeModelSerializer(TicketCommentITILSolutionAddModelSerializer):

    pass



class TicketCommentITILSolutionTriageModelSerializer(TicketCommentITILModelSerializer):
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
            # 'private',
            'duration',
            # 'is_template',
            # 'source',
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

    is_triage: bool = True

    def validate_triage(self, attrs):

        return attrs



class TicketCommentITILTaskAddModelSerializer(TicketCommentITILModelSerializer):
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



class TicketCommentITILTaskChangeModelSerializer(TicketCommentITILTaskAddModelSerializer):

    pass



class TicketCommentITILTaskTriageModelSerializer(TicketCommentITILModelSerializer):
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

    is_triage: bool = True

    def validate_triage(self, attrs):

        return attrs



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
