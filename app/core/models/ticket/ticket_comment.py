from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models import TenancyObject, Team

from core.lib.slash_commands import SlashCommands

from .ticket import Ticket
from .ticket_comment_category import TicketCommentCategory



class TicketComment(
    SlashCommands,
    TenancyObject,
):

    save_model_history: bool = False

    class Meta:

        ordering = [
            'created',
            'ticket',
            'parent_id'
        ]

        unique_together = ('external_system', 'external_ref',)

        verbose_name = "Ticket Comment"

        verbose_name_plural = "Ticket Comments"



    class CommentSource(models.IntegerChoices):
        """Source of the comment"""

        DIRECT   = '1', 'Direct'
        EMAIL    = '2', 'E-Mail'
        HELPDESK = '3', 'Helpdesk'
        PHONE    = '4', 'Phone'


    class CommentStatus(models.IntegerChoices):
        """Comment Completion Status"""

        TODO = '1', 'To Do'
        DONE = '2', 'Done'


    class CommentType(models.IntegerChoices):
        """        
        Comment types are as follows:

        - Action

        - Comment

        - Solution

        - Notification

        ## Action

        An action comment is for the tracking of what has occured to the ticket.

        ## Comment

        This is the default comment type and is what would be normally used.

        ## Solution

        This type of comment is an ITSM comment and is used as the means for solving the ticket.\
        
        ## Notification

        This type of comment is intended to be used to send a notification to subscribed users.
        """

        ACTION       = '1', 'Action'
        COMMENT      = '2', 'Comment'
        TASK         = '3', 'Task'
        NOTIFICATION = '4', 'Notification'
        SOLUTION     = '5', 'Solution'


    def validation_comment_type(field):

        if not field:
            raise ValidationError('Comment Type must be set')


    def validation_ticket_id(field):

        if not field:
            raise ValidationError('Ticket ID is required')


    model_notes = None

    is_global = None


    id = models.AutoField(
        blank=False,
        help_text = 'Comment ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    parent = models.ForeignKey(
        'self',
        blank= True,
        default = None,
        help_text = 'Parent ID for creating discussion threads',
        null = True,
        on_delete = models.DO_NOTHING,
        verbose_name = 'Parent Comment',
    )

    ticket = models.ForeignKey(
        Ticket,
        blank= True,
        default = None,
        help_text = 'Ticket this comment belongs to',
        null = True,
        on_delete = models.CASCADE,
        validators = [ validation_ticket_id ],
        verbose_name = 'Ticket',
    )


    external_ref = models.IntegerField(
        blank = True,
        default=None,
        help_text = 'External System reference',
        null=True,
        verbose_name = 'Reference Number',
    ) # external reference or null. i.e. github issue number

    external_system = models.IntegerField(
        blank = True,
        choices=Ticket.Ticket_ExternalSystem,
        default=None,
        help_text = 'External system this item derives',
        null=True,
        verbose_name = 'External System',
    ) 

    comment_type = models.IntegerField(
        blank = False,
        choices =CommentType,
        default = CommentType.COMMENT,
        help_text = 'The type of comment this is',
        validators = [ validation_comment_type ],
        verbose_name = 'Type',
    ) 

    body = models.TextField(
        blank = False,
        help_text = 'Comment contents',
        null = False,
        verbose_name = 'Comment',
    )

    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()

    private = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this comment private',
        null = False,
        verbose_name = 'Private',
    )

    duration = models.IntegerField(
        blank = False,
        default = 0,
        help_text = 'Time spent in seconds',
        null = False,
        verbose_name = 'Duration',
    )

    category = models.ForeignKey(
        TicketCommentCategory,
        blank= True,
        default = None,
        help_text = 'Category of the comment',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Category',
    )

    template = models.ForeignKey(
        'self',
        blank= True,
        default = None,
        help_text = 'Comment Template to use',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'comment_template',
        verbose_name = 'Template',
    )

    is_template = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this comment a template',
        null = False,
        verbose_name = 'Template',
    )

    source = models.IntegerField(
        blank = False,
        choices =CommentSource,
        default = CommentSource.DIRECT,
        help_text = 'Origin type for this comment',
        # validators = [ validation_ticket_type ],
        verbose_name = 'Source',
    ) 

    status = models.IntegerField( # will require validation by comment type as status for types will be different
        blank = False,
        choices=CommentStatus,
        default = CommentStatus.TODO,
        help_text = 'Status of comment',
        # null=True,
        verbose_name = 'Status',
    ) 

    responsible_user = models.ForeignKey(
        User,
        blank= True,
        default = None,
        help_text = 'User whom is responsible for the completion of comment',
        on_delete = models.DO_NOTHING,
        related_name = 'comment_responsible_user',
        null = True,
        verbose_name = 'Responsible User',
    )

    responsible_team = models.ForeignKey(
        Team,
        blank= True,
        default = None,
        help_text = 'Team whom is responsible for the completion of comment',
        on_delete = models.DO_NOTHING,
        related_name = 'comment_responsible_team',
        null = True,
        verbose_name = 'Responsible Team',
    )

    user = models.ForeignKey(
        User,
        blank= False,
        help_text = 'Who made the comment',
        null = True,
        on_delete = models.DO_NOTHING,
        related_name = 'comment_user',
        verbose_name = 'User',
    )

    date_closed = models.DateTimeField(
        blank = True,
        help_text = 'Date ticket closed',
        null = True,
        verbose_name = 'Closed Date',
    )

    planned_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned start date.',
        null = True,
        verbose_name = 'Planned Start Date',
    )

    planned_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned finish date',
        null = True,
        verbose_name = 'Planned Finish Date',
    )

    real_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Real start date',
        null = True,
        verbose_name = 'Real Start Date',
    )

    real_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Real finish date',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    # this model is not intended to be viewable on its
    # own page due to being a sub model
    page_layout: list = []


    # this model is not intended to be viewable via
    # a table as it's a sub-model
    table_fields: list = []


    common_fields: list(str()) = [
        'body',
        'duration',
        'user',
        'ticket',
        'parent',
        'comment_type',
    ]

    common_itsm_fields: list(str()) = common_fields + [
        'category',
        'source',
        'template',

    ]

    fields_itsm_task: list(str()) = common_itsm_fields + [
        'status',
        'responsible_user',
        'responsible_team',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]

    fields_itsm_notification: list(str()) = common_itsm_fields + [
        'status',
        'responsible_user',
        'responsible_team',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]

    fields_itsm_incident: list(str()) = common_itsm_fields + [

    ]

    fields_itsm_problem: list(str()) = common_itsm_fields + [

    ]

    fields_itsm_change: list(str()) = common_itsm_fields + [
        
    ]


    common_git_fields: list(str()) = common_fields + [

    ]

    fields_git_issue: list(str()) = common_fields + [

    ]

    fields_git_merge_request: list(str()) = common_fields + [

    ]

    fields_project_task: list(str()) = common_fields + [
        'category',
        'urgency',
        'status',
        'impact',
        'priority',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]

    fields_comment_task: list(str()) = common_itsm_fields + [
        'status',
        'responsible_user',
        'responsible_team',
        'planned_start_date',
        'planned_finish_date',
        'real_start_date',
        'real_finish_date',
    ]


    @property
    def action_comment(self):

        return self.user.username + ' ' + self.body + ' on ' +  str(self.created)


    @property
    def comment_template_queryset(self):

        query = TicketComment.objects.filter(
                is_template = True,
                comment_type = self.comment_type,
                )
        
        return query


    def get_url( self, request = None ) -> str:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        kwargs: dict = {
            'ticket_id': self.ticket.id,
            'pk': self.id
        }

        url_name: str = '_api_v2_ticket_comment'

        if getattr(self.parent, 'id', None):

            kwargs: dict = {
                'ticket_id': self.ticket.id,
                'parent_id': self.parent.id,
                'pk': self.id
            }

            url_name: str = '_api_v2_ticket_comment_threads'


        if request:

            return reverse(f"v2:{url_name}-detail", request=request, kwargs = kwargs )

        return reverse(f"v2:{url_name}-detail", kwargs = kwargs )



    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.ticket

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.organization = self.ticket.organization

        self.body = self.slash_command(self.body)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if self.comment_type == self.CommentType.SOLUTION:

            update_ticket =  self.ticket.__class__.objects.get(pk=self.ticket.id)
            update_ticket.status = int(Ticket.TicketStatus.All.SOLVED.value)

            update_ticket.save()


    @property
    def threads(self):

        return TicketComment.objects.filter(
            parent = self.id
        )
