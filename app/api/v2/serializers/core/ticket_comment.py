from django.urls import reverse

from rest_framework import serializers
from rest_framework.fields import empty

from core.models.ticket.ticket_comment import Ticket, TicketComment

from access.serializers.organization import OrganizationBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from api.v2.serializers.base.user import UserBaseSerializer



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


    # operating_system = OperatingSystemModelSerializer(source='id', many=False, read_only=False)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        request = self.context.get('request')

        if item.ticket.ticket_type == item.ticket.__class__.TicketType.CHANGE:

            view_name = '_api_itim_change_ticket_comments'
        
        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.INCIDENT:

            view_name = '_api_itim_incident_ticket_comments'

        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.PROBLEM:

            view_name = '_api_itim_problem_ticket_comments'

        elif item.ticket.ticket_type == item.ticket.__class__.TicketType.REQUEST:

            # view_name = '_api_assistance_request_ticket_comments'
            view_name = '_api_v2_assistance_request_ticket_comments'

        else:

            raise ValueError('Serializer unable to obtain ticket type')


        # return request.build_absolute_uri(
        #     reverse('API:' + view_name + '-detail',
        #         kwargs={
        #             'ticket_id': item.ticket.id,
        #             'pk': item.id
        #         }
        #     )
        # )

        return {
            '_self': request.build_absolute_uri(
            reverse('API:' + view_name + '-detail',
            # reverse('API_api_v2_device-detail',
                kwargs={
                    'ticket_id': item.ticket.id,
                    'pk': item.id
                }
            )
        ),
            # 'history': 'ToDo',
            # 'notes': 'ToDo',
            # 'services': 'ToDo',
            # 'software': reverse("API:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            # 'tickets': 'ToDo'
        }

    # rendered_config = serializers.SerializerMethodField('get_rendered_config')
    # rendered_config = serializers.JSONField(source='get_configuration')


    # def get_rendered_config(self, item):

    #     return item.get_configuration(0)


    class Meta:

        model = TicketComment

        fields = '__all__'

        fields =  [
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

            # 'display_name',
            # 'name',
            # 'device_type',
            # # 'operating_system',
            # 'model_notes',
            # 'serial_number',
            # 'uuid',
            # 'is_global',
            # 'is_virtual',
            # 'device_model',
            # 'config',
            # 'rendered_config',
            # 'inventorydate',
            
            # 
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'inventorydate',
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

                    self.fields.fields['ticket'].initial = int(self._kwargs['context']['view'].kwargs['ticket_id'])

                    self.fields.fields['comment_type'].initial = TicketComment.CommentType.COMMENT

                    self.fields.fields['user'].initial = kwargs['context']['request']._user.id

        super().__init__(instance=instance, data=data, **kwargs)



class TicketCommentViewSerializer(TicketCommentModelSerializer):

    # device_model = DeviceModelBaseSerializer(many=False, read_only=True)

    # device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    user = UserBaseSerializer()

    responsible_user = UserBaseSerializer()

    responsible_team = TeamBaseSerializer()




# class TicketCommentSerializer(serializers.ModelSerializer):


#     url = serializers.SerializerMethodField('get_url_ticket_comment')

#     def get_url_ticket_comment(self, item):

#         request = self.context.get('request')

#         if item.ticket.ticket_type == item.ticket.__class__.TicketType.CHANGE:

#             view_name = '_api_itim_change_ticket_comments'
        
#         elif item.ticket.ticket_type == item.ticket.__class__.TicketType.INCIDENT:

#             view_name = '_api_itim_incident_ticket_comments'

#         elif item.ticket.ticket_type == item.ticket.__class__.TicketType.PROBLEM:

#             view_name = '_api_itim_problem_ticket_comments'

#         elif item.ticket.ticket_type == item.ticket.__class__.TicketType.REQUEST:

#             view_name = '_api_assistance_request_ticket_comments'

#         else:

#             raise ValueError('Serializer unable to obtain ticket type')


#         return request.build_absolute_uri(
#             reverse('API:' + view_name + '-detail',
#                 kwargs={
#                     'ticket_id': item.ticket.id,
#                     'pk': item.id
#                 }
#             )
#         )



#     class Meta:
#         model = TicketComment
        
#         fields = '__all__'

    