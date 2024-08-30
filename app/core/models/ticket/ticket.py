from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.forms import ValidationError

from access.fields import AutoCreatedField
from access.models import TenancyObject, Team

from core.middleware.get_request import get_request

from .markdown import TicketMarkdown

from project_management.models.projects import Project



class TicketValues:

    
        _DRAFT_INT    = '1'
        _NEW_INT      = '2'

        _ASSIGNED_INT = '3'
        _CLOSED_INT   = '4'
        _INVALID_INT  = '5'

        #
        # ITSM statuses
        #

        # Requests / Incidents / Problems / Changed
        _ASSIGNED_PLANNING_INT = '6'
        _PENDING_INT           = '7'

        # Requests / Incidents / Problems
        _SOLVED_INT            = '8'

        # Problem

        _OBSERVATION_INT = '9'

        # Problems / Changes

        _ACCEPTED_INT = '10'

        # Changes

        _EVALUATION_INT    = '11'
        _APPROVALS_INT     = '12'
        _TESTING_INT       = '13'
        _QUALIFICATION_INT = '14'
        _APPLIED_INT       = '15'
        _REVIEW_INT        = '16'
        _CANCELLED_INT     = '17'
        _REFUSED_INT       = '18'



    
        _DRAFT_STR    = 'Draft'
        _NEW_STR      = 'New'

        _ASSIGNED_STR = 'Assigned'
        _CLOSED_STR   = 'Closed'
        _INVALID_STR  = 'Invalid'

        #
        # ITSM statuses
        #

        # Requests / Incidents / Problems / Changed
        _ASSIGNED_PLANNING_STR = 'Assigned (Planning)'
        _PENDING_STR           = 'Pending'

        # Requests / Incidents / Problems
        _SOLVED_STR            = 'Solved'

        # Problem

        _OBSERVATION_STR = 'Under Observation'

        # Problems / Changes

        _ACCEPTED_STR = 'Accepted'

        # Changes

        _EVALUATION_STR    = 'Evaluation'
        _APPROVALS_STR     = 'Approvals'
        _TESTING_STR       = 'Testing'
        _QUALIFICATION_STR = 'Qualification'
        _APPLIED_STR       = 'Applied'
        _REVIEW_STR        = 'Review'
        _CANCELLED_STR     = 'Cancelled'
        _REFUSED_STR       = 'Refused'



class TicketCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Ticket ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoCreatedField()



class Ticket(
    TenancyObject,
    TicketCommonFields,
    TicketMarkdown,
):


    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('add_ticket_request', 'Can add a request ticket'),
            ('change_ticket_request', 'Can change any request ticket'),
            ('delete_ticket_request', 'Can delete a request ticket'),
            ('import_ticket_request', 'Can import a request ticket'),
            ('purge_ticket_request', 'Can purge a request ticket'),
            ('triage_ticket_request', 'Can triage all request ticket'),
            ('view_ticket_request', 'Can view all request ticket'),

            ('add_ticket_incident', 'Can add a incident ticket'),
            ('change_ticket_incident', 'Can change any incident ticket'),
            ('delete_ticket_incident', 'Can delete a incident ticket'),
            ('import_ticket_incident', 'Can import a incident ticket'),
            ('purge_ticket_incident', 'Can purge a incident ticket'),
            ('triage_ticket_incident', 'Can triage all incident ticket'),
            ('view_ticket_incident', 'Can view all incident ticket'),

            ('add_ticket_problem', 'Can add a problem ticket'),
            ('change_ticket_problem', 'Can change any problem ticket'),
            ('delete_ticket_problem', 'Can delete a problem ticket'),
            ('import_ticket_problem', 'Can import a problem ticket'),
            ('purge_ticket_problem', 'Can purge a problem ticket'),
            ('triage_ticket_problem', 'Can triage all problem ticket'),
            ('view_ticket_problem', 'Can view all problem ticket'),

            ('add_ticket_change', 'Can add a change ticket'),
            ('change_ticket_change', 'Can change any change ticket'),
            ('delete_ticket_change', 'Can delete a change ticket'),
            ('import_ticket_change', 'Can import a change ticket'),
            ('purge_ticket_change', 'Can purge a change ticket'),
            ('triage_ticket_change', 'Can triage all change ticket'),
            ('view_ticket_change', 'Can view all change ticket'),
        ]

        verbose_name = "Ticket"

        verbose_name_plural = "Tickets"



    class Ticket_ExternalSystem(models.IntegerChoices): # <null|github|gitlab>
        GITHUB   = '1', 'Github'
        GITLAB   = '2', 'Gitlab'

        CUSTOM_1 = '9999', 'Custom #1 (Imported)'
        CUSTOM_2 = '9998', 'Custom #2 (Imported)'
        CUSTOM_3 = '9997', 'Custom #3 (Imported)'
        CUSTOM_4 = '9996', 'Custom #4 (Imported)'
        CUSTOM_5 = '9995', 'Custom #5 (Imported)'
        CUSTOM_6 = '9994', 'Custom #6 (Imported)'
        CUSTOM_7 = '9993', 'Custom #7 (Imported)'
        CUSTOM_8 = '9992', 'Custom #8 (Imported)'
        CUSTOM_9 = '9991', 'Custom #9 (Imported)'



    class TicketStatus: # <draft|open|closed|in progress|assigned|solved|invalid>
        """ Ticket Status

        Status of the ticket. By design, not all statuses are available for ALL ticket types.

        ## Request / Incident ticket 

        - Draft
        - New
        - Assigned
        - Assigned (Planned)
        - Pending
        - Solved
        - Closed


        ## Problem Ticket

        - Draft
        - New
        - Accepted
        - Assigned
        - Assigned (Planned)
        - Pending
        - Solved
        - Under Observation
        - Closed

        ## Change Ticket

        - Draft
        - New
        - Evaluation
        - Approvals
        - Accepted
        - Pending
        - Testing
        - Qualification
        - Applied
        - Review
        - Closed
        - Cancelled
        - Refused

        """

        class All(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR

            # Problem
            ACCEPTED          = TicketValues._ACCEPTED_INT, TicketValues._ACCEPTED_STR
            OBSERVATION       = TicketValues._OBSERVATION_INT, TicketValues._OBSERVATION_STR

            # change
            EVALUATION    = TicketValues._EVALUATION_INT, TicketValues._EVALUATION_STR
            APPROVALS     = TicketValues._APPROVALS_INT, TicketValues._APPROVALS_STR
            TESTING       = TicketValues._TESTING_INT, TicketValues._TESTING_STR
            QUALIFICATION = TicketValues._QUALIFICATION_INT, TicketValues._QUALIFICATION_STR
            APPLIED       = TicketValues._APPLIED_INT, TicketValues._APPLIED_STR
            REVIEW        = TicketValues._REVIEW_INT, TicketValues._REVIEW_STR
            CANCELLED     = TicketValues._CANCELLED_INT, TicketValues._CANCELLED_STR
            REFUSED       = TicketValues._REFUSED_INT, TicketValues._REFUSED_STR



        class Request(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR



        class Incident(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR



        class Problem(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ACCEPTED          = TicketValues._ACCEPTED_INT, TicketValues._ACCEPTED_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
            OBSERVATION       = TicketValues._OBSERVATION_INT, TicketValues._OBSERVATION_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR



        class Change(models.IntegerChoices):
 
            DRAFT         = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW           = TicketValues._NEW_INT, TicketValues._NEW_STR
            EVALUATION    = TicketValues._EVALUATION_INT, TicketValues._EVALUATION_STR
            APPROVALS     = TicketValues._APPROVALS_INT, TicketValues._APPROVALS_STR
            ACCEPTED      = TicketValues._ACCEPTED_INT, TicketValues._ACCEPTED_STR
            PENDING       = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            TESTING       = TicketValues._TESTING_INT, TicketValues._TESTING_STR
            QUALIFICATION = TicketValues._QUALIFICATION_INT, TicketValues._QUALIFICATION_STR
            APPLIED       = TicketValues._APPLIED_INT, TicketValues._APPLIED_STR
            REVIEW        = TicketValues._REVIEW_INT, TicketValues._REVIEW_STR
            CLOSED        = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            CANCELLED     = TicketValues._CANCELLED_INT, TicketValues._CANCELLED_STR
            REFUSED       = TicketValues._REFUSED_INT, TicketValues._REFUSED_STR


        class Git(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR


        class ProjectTask(models.IntegerChoices):

            DRAFT             = TicketValues._DRAFT_INT, TicketValues._DRAFT_STR
            NEW               = TicketValues._NEW_INT, TicketValues._NEW_STR
            ASSIGNED          = TicketValues._ASSIGNED_INT, TicketValues._ASSIGNED_STR
            ASSIGNED_PLANNING = TicketValues._ASSIGNED_PLANNING_INT, TicketValues._ASSIGNED_PLANNING_STR
            PENDING           = TicketValues._PENDING_INT, TicketValues._PENDING_STR
            SOLVED            = TicketValues._SOLVED_INT, TicketValues._SOLVED_STR
            CLOSED            = TicketValues._CLOSED_INT, TicketValues._CLOSED_STR
            INVALID           = TicketValues._INVALID_INT, TicketValues._INVALID_STR




    class TicketType(models.IntegerChoices):
        """Type of the ticket"""

        REQUEST       = '1', 'Request'
        INCIDENT      = '2', 'Incident'
        CHANGE        = '3', 'Change'
        PROBLEM       = '4', 'Problem'
        ISSUE         = '5', 'Issue'
        MERGE_REQUEST = '6', 'Merge Request'
        PROJECT_TASK  = '7', 'Project Task'



    class TicketUrgency(models.IntegerChoices): # <null|github|gitlab>
        VERY_LOW  = '1', 'Very Low'
        LOW       = '2', 'Low'
        MEDIUM    = '3', 'Medium'
        HIGH      = '4', 'High'
        VERY_HIGH = '5', 'Very High'



    class TicketImpact(models.IntegerChoices):
        VERY_LOW  = '1', 'Very Low'
        LOW       = '2', 'Low'
        MEDIUM    = '3', 'Medium'
        HIGH      = '4', 'High'
        VERY_HIGH = '5', 'Very High'



    class TicketPriority(models.IntegerChoices):
        VERY_LOW  = '1', 'Very Low'
        LOW       = '2', 'Low'
        MEDIUM    = '3', 'Medium'
        HIGH      = '4', 'High'
        VERY_HIGH = '5', 'Very High'
        MAJOR     = '6', 'Major'



    def validation_ticket_type(field):

        if not field:
            raise ValidationError('Ticket Type must be set')


    def validation_title(field):

        if not field:
            raise ValueError


    model_notes = None

    is_global = None


    status = models.IntegerField( # will require validation by ticket type as status for types will be different
        blank = False,
        choices=TicketStatus.All,
        default = TicketStatus.All.NEW,
        help_text = 'Status of ticket',
        # null=True,
        verbose_name = 'Status',
    ) 

    # category = models.CharField(
    #     blank = False,
    #     help_text = "Category of the Ticket",
    #     max_length = 50,
    #     unique = True,
    #     verbose_name = 'Category',
    # )

    title = models.CharField(
        blank = False,
        help_text = "Title of the Ticket",
        max_length = 50,
        unique = True,
        verbose_name = 'Title',
    )

    description = models.TextField(
        blank = False,
        default = None,
        help_text = 'Ticket Description',
        null = False,
        verbose_name = 'Description',
    ) # text, markdown


    urgency = models.IntegerField(
        blank = True,
        choices=TicketUrgency,
        default=TicketUrgency.VERY_LOW,
        help_text = 'How urgent is this tickets resolution for the user?',
        null=True,
        verbose_name = 'Urgency',
    ) 

    impact = models.IntegerField(
        blank = True,
        choices=TicketImpact,
        default=TicketImpact.VERY_LOW,
        help_text = 'End user assessed impact',
        null=True,
        verbose_name = 'Impact',
    ) 

    priority = models.IntegerField(
        blank = True,
        choices=TicketPriority,
        default=TicketPriority.VERY_LOW,
        help_text = 'What priority should this ticket for its completion',
        null=True,
        verbose_name = 'Priority',
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
        choices=Ticket_ExternalSystem,
        default=None,
        help_text = 'External system this item derives',
        null=True,
        verbose_name = 'External System',
    ) 


    ticket_type = models.IntegerField(
        blank = False,
        choices=TicketType,
        help_text = 'The type of ticket this is',
        validators = [ validation_ticket_type ],
        verbose_name = 'Type',
    ) 


    project = models.ForeignKey(
        Project,
        blank= True,
        help_text = 'Assign to a project',
        null = True,
        on_delete = models.DO_NOTHING,
        verbose_name = 'Project',
    )


    opened_by = models.ForeignKey(
        User,
        blank= False,
        help_text = 'Who is the ticket for',
        null = False,
        on_delete = models.DO_NOTHING,
        related_name = 'opened_by',
        verbose_name = 'Opened By',
    )


    subscribed_users = models.ManyToManyField(
        User,
        blank= True,
        help_text = 'Subscribe a User(s) to the ticket to receive updates',
        related_name = 'subscribed_users',
        symmetrical = False,
        verbose_name = 'Subscribed User(s)',
    )


    subscribed_teams = models.ManyToManyField(
        Team,
        blank= True,
        help_text = 'Subscribe a Team(s) to the ticket to receive updates',
        related_name = 'subscribed_teams',
        symmetrical = False,
        verbose_name = 'Subscribed Team(s)',
    )

    assigned_users = models.ManyToManyField(
        User,
        blank= True,
        help_text = 'Assign the ticket to a User(s)',
        related_name = 'assigned_users',
        symmetrical = False,
        verbose_name = 'Assigned User(s)',
    )

    assigned_teams = models.ManyToManyField(
        Team,
        blank= True,
        help_text = 'Assign the ticket to a Team(s)',
        related_name = 'assigned_teams',
        symmetrical = False,
        verbose_name = 'Assigned Team(s)',
    )

    is_deleted = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is the ticket deleted? And ready to be purged',
        null = False,
        verbose_name = 'Deleted',
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


    # ?? date_edit date of last edit

    def __str__(self):

        return self.title

    common_fields: list(str()) = [
        'organization',
        'title',
        'description',
        'opened_by',
        'ticket_type'
    ]

    common_itsm_fields: list(str()) = common_fields + [
        'urgency',

    ]

    fields_itsm_request: list(str()) = common_itsm_fields + [

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

    tech_fields = [
        'category',
        'project',
        'assigned_users',
        'assigned_teams',
        'subscribed_teams',
        'subscribed_users',
        'status',
        'urgency',
        'impact',
        'priority',
        'planned_start_date',
        'planned_finish_date',
    ]


    @property
    def comments(self):

        from core.models.ticket.ticket_comment import TicketComment

        return TicketComment.objects.filter(
            ticket = self.id,
            parent = None,
        )


    @property
    def markdown_description(self) -> str:

        return self.render_markdown(self.description)

    @property
    def related_tickets(self) -> list(dict()):

        related_tickets: list() = []

        query = RelatedTickets.objects.filter(
            Q(from_ticket_id=self.id)
                |
            Q(to_ticket_id=self.id)
        )

        for related_ticket in query:


            how_related:str = str(related_ticket.get_how_related_display()).lower()
            ticket_title: str = related_ticket.to_ticket_id.title


            if related_ticket.to_ticket_id_id == self.id:

                if str(related_ticket.get_how_related_display()).lower() == 'blocks':

                    how_related = 'blocked by'
                    ticket_title = related_ticket.from_ticket_id.title

                elif str(related_ticket.get_how_related_display()).lower() == 'blocked by':

                    how_related = 'blocks'


            related_tickets += [
                {
                    'id': related_ticket.id,
                    'type': related_ticket.to_ticket_id.get_ticket_type_display().lower(),
                    'title': ticket_title,
                    'how_related': how_related.replace(' ', '_'),
                    'icon_filename': str('icons/ticket/ticket_' + how_related.replace(' ', '_') + '.svg')
                }
            ]

        return related_tickets


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        before = {}

        try:
            before = self.__class__.objects.get(pk=self.pk).__dict__.copy()
        except Exception:
            pass

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        after = self.__dict__.copy()

        changed_fields: list = []

        for field, value in before.items():

            if before[field] != after[field] and field != '_state':

                changed_fields = changed_fields + [ field ]

        request = get_request()

        from core.models.ticket.ticket_comment import TicketComment

        for field in changed_fields:

            comment_field_value: str = None

            if field == 'impact':

                comment_field_value = f"changed {field} to {self.get_impact_display()}"

            if field == 'urgency':

                comment_field_value = f"changed {field} to {self.get_urgency_display()}"

            if field == 'priority':

                comment_field_value = f"changed {field} to {self.get_priority_display()}"


            if field == 'status':

                comment_field_value = f"changed {field} to {self.get_status_display()}"

            if field == 'project_id':

                comment_field_value = f"changed {field.replace('_id','')} to {self.project}"


            if comment_field_value:

                comment = TicketComment.objects.create(
                    ticket = self,
                    comment_type = TicketComment.CommentType.ACTION,
                    body = comment_field_value,
                    source = TicketComment.CommentSource.DIRECT,
                    user = request.user,
                )

                comment.save()


class RelatedTickets(TenancyObject):

    class Meta:

        ordering = [
            'id'
        ]

    class Related(models.IntegerChoices):
        RELATED = '1', 'Related'

        BLOCKS = '2', 'Blocks'

        BLOCKED_BY = '3', 'Blocked By'

    is_global = None

    model_notes = None

    id = models.AutoField(
        blank=False,
        help_text = 'Ticket ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    from_ticket_id = models.ForeignKey(
        Ticket,
        blank= False,
        help_text = 'This Ticket',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'from_ticket_id',
        verbose_name = 'Ticket',
    )

    how_related = models.IntegerField(
        blank = False,
        choices = Related,
        help_text = 'How is the ticket related',
        verbose_name = 'How Related',
    )

    to_ticket_id = models.ForeignKey(
        Ticket,
        blank= False,
        help_text = 'The Related Ticket',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'to_ticket_id',
        verbose_name = 'Related Ticket',
    )


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.from_ticket_id


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if self.how_related == self.Related.BLOCKED_BY:

            comment_field_value_from = f" added #{self.from_ticket_id.id} as blocked by #{self.to_ticket_id.id}"
            comment_field_value_to = f" added #{self.to_ticket_id.id} as blocking #{self.from_ticket_id.id}"

        elif self.how_related == self.Related.BLOCKS:

            comment_field_value_from = f" added #{self.from_ticket_id.id} as blocking #{self.to_ticket_id.id}"
            comment_field_value_to = f" added #{self.to_ticket_id.id} as blocked by #{self.from_ticket_id.id}"

        elif self.how_related == self.Related.RELATED:

            comment_field_value_from = f" added #{self.from_ticket_id.id} as related to #{self.to_ticket_id.id}"
            comment_field_value_to = f" added #{self.to_ticket_id.id} as related to #{self.from_ticket_id.id}"


        request = get_request()

        from core.models.ticket.ticket_comment import TicketComment

        if comment_field_value_from:

            comment = TicketComment.objects.create(
                ticket = self.from_ticket_id,
                comment_type = TicketComment.CommentType.ACTION,
                body = comment_field_value_from,
                source = TicketComment.CommentSource.DIRECT,
                user = request.user,
            )

            comment.save()


        if comment_field_value_to:

            comment = TicketComment.objects.create(
                ticket = self.to_ticket_id,
                comment_type = TicketComment.CommentType.ACTION,
                body = comment_field_value_to,
                source = TicketComment.CommentSource.DIRECT,
                user = request.user,
            )

            comment.save()

