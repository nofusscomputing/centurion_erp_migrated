from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from app.serializers.user import UserBaseSerializer

from api.exceptions import UnknownTicketType

from core import exceptions as centurion_exception
from core.models.ticket.ticket import Ticket

from core.fields.badge import Badge, BadgeField
from core.serializers.ticket_category import TicketCategoryBaseSerializer



class TicketBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item):

        context = self.context.copy()

        ticket_type = str(item.get_ticket_type_display()).lower().replace(' ', '_')

        if ticket_type == 'project_task':

            kwargs: dict = {
                'project_id': item.project.id,
                'pk': item.pk
            }

        else:

            kwargs: dict = {
                'pk': item.pk
            }


        return reverse(
            "v2:_api_v2_ticket_" + ticket_type + "-detail",
            request=context['view'].request,
            kwargs = kwargs
        )


    class Meta:

        model = Ticket

        fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]


class TicketModelSerializer(TicketBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        context = self.context.copy()

        ticket_type = str(item.get_ticket_type_display()).lower().replace(' ', '_')

        if ticket_type == 'project_task':

            kwargs: dict = {
                'project_id': item.project.id,
                'pk': item.pk
            }

        else:

            kwargs: dict = {
                'pk': item.pk
            }

        url_dict: dict = {
            '_self': reverse(
                "v2:_api_v2_ticket_" + ticket_type + "-detail",
                request=context['view'].request,
                kwargs = kwargs
            ),
            'comments': reverse('v2:_api_v2_ticket_comments-list', request=context['view'].request, kwargs={'ticket_id': item.pk}),
            'linked_items': reverse("v2:_api_v2_ticket_linked_item-list", request=context['view'].request, kwargs={'ticket_id': item.pk}),
        }

        if item.project:

            url_dict.update({
                'project': reverse("v2:_api_v2_project-list", request=context['view'].request, kwargs={}),
            })

        if item.category:

            url_dict.update({
            'ticketcategory': reverse(
                'v2:_api_v2_ticket_category-list',
                request=context['view'].request,
                kwargs={},
            ) + '?' + ticket_type + '=true',
            })


        url_dict.update({
            'related_tickets': reverse("v2:_api_v2_ticket_related-list", request=context['view'].request, kwargs={'ticket_id': item.pk}),
        })


        return url_dict


    duration = serializers.IntegerField(source='duration_ticket', read_only=True)

    status_badge = BadgeField(label='Status')


    class Meta:
        """Ticket Model Base Meta

        This class specifically has only `id` in fields and all remaining fields
        as ready only so as to prevent using this serializer directly. The intent
        is that for each ticket type there is a seperate serializer for that ticket
        type.

        These serializers are for items that are common for ALL tickets.
        """

        model = Ticket

        fields = [
            'id',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'title',
            'description',
            'estimate',
            'duration',
            'urgency',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'opened_by',
            'organization',
            'project',
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



    def validate_field_organization(self) -> bool:
        """Check `organization field`

        Raises:
            ValidationError: user tried to change the organization

        Returns:
            True (bool): OK
            False (bool): User tried to edit the organization
        """

        is_valid: bool = True

        if self.instance is not None:

            if self.instance.pk is not None:

                if 'organization' in self.get_user_changed_fields:

                    if self.field_edited('organization'):

                        is_valid = False

                        centurion_exception.ValidationError(
                            detail = 'cant edit field: organization',
                            code = 'cant_edit_field_organization',
                        )


        return is_valid


    def validate_field_milestone( self ) -> bool:

        is_valid: bool = False

        if self.instance is not None:

            if self.instance.milestone is None:

                return True

            else:

                if self.instance.project is None:

                    raise centurion_exception.ValidationError(
                        details = 'Milestones require a project',
                        code = 'milestone_requires_project',
                    )

                    return False

                if self.instance.project.id == self.instance.milestone.project.id:

                    return True

                else:

                    raise centurion_exception.ValidationError(
                        detail = 'Milestone must be from the same project',
                        code = 'milestone_same_project',
                    )

        return is_valid


    def validate(self, data):

        if 'view' in self._context:

            if self._context['view'].action == 'create':

                if hasattr(self._context['view'], 'request'):

                    data['opened_by_id'] = self._context['view'].request.user.id


            if hasattr(self._context['view'], '_ticket_type_id'):

                data['ticket_type'] = self._context['view']._ticket_type_id

            else:

                raise UnknownTicketType()

        self.validate_field_organization()

        self.validate_field_milestone()

        return data


class TicketViewSerializer(TicketModelSerializer):

    assigned_teams = TeamBaseSerializer(many=True)

    assigned_users = UserBaseSerializer(many=True, label='Assigned Users')

    category = TicketCategoryBaseSerializer()

    opened_by = UserBaseSerializer()

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    subscribed_teams = TeamBaseSerializer(many=True)

    subscribed_users = UserBaseSerializer(many=True)
