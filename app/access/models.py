from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.forms import ValidationError

from rest_framework.reverse import reverse

from .fields import *

from core.middleware.get_request import get_request
from core.mixin.history_save import SaveHistory


class Organization(SaveHistory):

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def save(self, *args, **kwargs):

        if self.slug == '_':
            self.slug = self.name.lower().replace(' ', '_')

        super().save(*args, **kwargs)

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this Organization',
        max_length = 50,
        unique = True,
        verbose_name = 'Name'
    )

    manager = models.ForeignKey(
        User,
        blank = False,
        help_text = 'Manager for this organization',
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = 'Manager'
    )

    model_notes = models.TextField(
        blank = True,
        default = None,
        help_text = 'Tid bits of information',
        null= True,
        verbose_name = 'Notes',
    )

    slug = AutoSlugField()

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def get_organization(self):
        return self

    def __str__(self):
        return self.name

    table_fields: list = [
        'nbsp',
        'name',
        'created',
        'modified',
        'nbsp'
    ]

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'name',
                        'manager',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                }
            ]
        },
        {
            "name": "Teams",
            "slug": "teams",
            "sections": [
                {
                    "layout": "table",
                    "field": "teams"
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        }
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse("v2:_api_v2_organization-detail", request=request, kwargs={'pk': self.id})

        return reverse("v2:_api_v2_organization-detail", kwargs={'pk': self.id})



class TenancyManager(models.Manager):
    """Multi-Tennant Object Manager

    This manager specifically caters for the multi-tenancy features of Centurion ERP.
    """


    def get_queryset(self):
        """ Fetch the data

        This function filters the data fetched from the database to that which is from the organizations
        the user is a part of.

        !!! danger "Requirement"
            This method may be overridden however must still be called from the overriding function. i.e. `super().get_queryset()`

        ## Workflow

        This functions workflow is as follows:

        - Fetch the user from the request

        - Check if the user is authenticated

        - Iterate over the users teams

        - Store unique organizations from users teams

        - return results

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        request = get_request()

        user_organizations: list(str()) = []


        if request:

            # user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

            user = request.user


            if user.is_authenticated:

                for team_user in TeamUsers.objects.filter(user=user):


                    if team_user.team.organization.name not in user_organizations:


                        if not user_organizations:

                            self.user_organizations = []

                        user_organizations += [ team_user.team.organization.id ]


                # if len(user_organizations) > 0 and not user.is_superuser and self.model.is_global is not None:
                if len(user_organizations) > 0 and not user.is_superuser:

                    if getattr(self.model, 'is_global', False) is True:

                        return super().get_queryset().filter(
                            models.Q(organization__in=user_organizations)
                            |
                            models.Q(is_global = True)
                        )

                    else:

                        return super().get_queryset().filter(
                            models.Q(organization__in=user_organizations)
                        )

        return super().get_queryset()



class TenancyObject(SaveHistory):
    """ Tenancy Model Abstrct class.

    This class is for inclusion wihtin **every** model within Centurion ERP.
    Provides the required fields, functions and methods for multi tennant objects.
    Unless otherwise stated, **no** object within this class may be overridden.

    Raises:
        ValidationError: User failed to supply organization
    """

    objects = TenancyManager()
    """ Multi-Tenanant Objects """

    class Meta:
        abstract = True


    def validatate_organization_exists(self):
        """Ensure that the user did provide an organization

        Raises:
            ValidationError: User failed to supply organization.
        """

        if not self:
            raise ValidationError('You must provide an organization')


    id = models.AutoField(
        blank=False,
        help_text = 'ID of the item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    organization = models.ForeignKey(
        Organization,
        blank = False,
        help_text = 'Organization this belongs to',
        null = False,
        on_delete = models.CASCADE,
        validators = [validatate_organization_exists],
        verbose_name = 'Organization'
    )

    is_global = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this a global object?',
        verbose_name = 'Global Object'
    )

    model_notes = models.TextField(
        blank = True,
        default = None,
        help_text = 'Tid bits of information',
        null = True,
        verbose_name = 'Notes',
    )

    def get_organization(self) -> Organization:
        return self.organization


    def get_url( self, request = None ) -> str:
        """Fetch the models URL

        If URL kwargs are required to generate the URL, define a `get_url_kwargs` that returns them.

        Args:
            request (object, optional): The request object that was made by the end user. Defaults to None.

        Returns:
            str: Canonical URL of the model if the `request` object was provided. Otherwise the relative URL. 
        """

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_{model_name}-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_{model_name}-detail", kwargs = self.get_url_kwargs() )


    def get_url_kwargs(self) -> dict:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        return {
            'pk': self.id
        }


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.organization is None:

            raise ValidationError('Organization not defined')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



class Team(Group, TenancyObject):

    class Meta:

        ordering = [ 'team_name' ]

        verbose_name = 'Team'

        verbose_name_plural = "Teams"


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.name = self.organization.name.lower().replace(' ', '_') + '_' + self.team_name.lower().replace(' ', '_')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    team_name = models.CharField(
        blank = False,
        help_text = 'Name to give this team',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'team_name',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
                {
                    "layout": "table",
                    "name": "Users",
                    "field": "users",
                },
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]

    table_fields: list = [
        'team_name',
        'modified',
        'created',
    ]


    def get_url( self, request = None ) -> str:

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_organization_team-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_organization_team-detail", kwargs = self.get_url_kwargs() )


    def get_url_kwargs(self) -> dict:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        return {
            'organization_id': self.organization.id,
            'pk': self.id
        }


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.organization


    def permission_list(self) -> list:

        permission_list = []

        for permission in self.permissions.all():

            if str(permission.content_type.app_label + '.' + permission.codename) in permission_list:
                continue

            permission_list += [ str(permission.content_type.app_label + '.' + permission.codename) ]

        return [permission_list, self.permissions.all()]


    def __str__(self):
        return self.team_name



class TeamUsers(SaveHistory):

    class Meta:

        ordering = ['user']

        verbose_name = "Team User"

        verbose_name_plural = "Team Users"


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this Team User',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    team = models.ForeignKey(
        Team,
        blank = False,
        help_text = 'Team user belongs to',
        null = False,
        on_delete=models.CASCADE,
        related_name="team",
        verbose_name = 'Team'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'User who will be added to the team',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'User'
    )

    manager = models.BooleanField(
        blank=True,
        default=False,
        help_text = 'Is this user to be a manager of this team',
        verbose_name='manager',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    page_layout: list = []

    table_fields: list = []


    def delete(self, using=None, keep_parents=False):
        """ Delete Team

        Overrides, post-action
            As teams are an extension of Groups, remove the user to the team.
        """

        super().delete(using=using, keep_parents=keep_parents)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)
        
        user.groups.remove(group)


    def get_organization(self) -> Organization:
        return self.team.organization


    def get_url( self, request = None ) -> str:

        url_kwargs: dict = {
            'organization_id': self.team.organization.id,
            'team_id': self.team.id,
            'pk': self.id
        }

        print(f'url kwargs are: {url_kwargs}')


        if request:

            return reverse(f"v2:_api_v2_organization_team_user-detail", request=request, kwargs = url_kwargs )

        return reverse(f"v2:_api_v2_organization_team_user-detail", kwargs = url_kwargs )


    def save(self, *args, **kwargs):
        """ Save Team

        Overrides, post-action
            As teams are an extension of groups, add the user to the matching group.
        """

        super().save(*args, **kwargs)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)

        user.groups.add(group) 


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.team

    def __str__(self):
        return self.user.username

