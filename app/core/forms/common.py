from django import forms
from django.db.models import Q

from access.models import Organization, TeamUsers



class CommonModelForm(forms.ModelForm):
    """ Abstract Form class for form inclusion

    This class exists so that common functions can be conducted against forms as they are loaded.
    """

    organization_field: str = 'organization'
    """ Organization Field
    
    Name of the field that contains Organizations.

    This field will be filtered to those that the user is part of.
    """


    def __init__(self, *args, **kwargs):
        """Form initialization.

        Initialize the form using the super classes first then continue to initialize the form using logic
        contained within this method.

        ## Tenancy Objects

        Fields that contain an attribute called `organization` will have the objects filtered to
        the organizations the user is part of. If the object has `is_global=True`, that object will not be
        filtered out.


        !!! danger "Requirement"
            This method may be overridden however must still be called from the overriding function. i.e. `super().__init__(*args, **kwargs)`
        """

        user = kwargs.pop('user', None)

        user_organizations: list([str]) = []
        user_organizations_id: list(int()) = []

        for team_user in TeamUsers.objects.filter(user=user):

            if team_user.team.organization.name not in user_organizations:

                if not user_organizations:

                    self.user_organizations = []

                user_organizations += [ team_user.team.organization.name ]
                user_organizations_id += [ team_user.team.organization.id ]

        new_kwargs: dict = {}

        for key, value in kwargs.items():

            if key != 'user':

                new_kwargs.update({key: value})

        super().__init__(*args, **new_kwargs)


        if len(user_organizations_id) > 0:

            for field_name in self.fields:

                field = self.fields[field_name]

                if hasattr(field, 'queryset'):

                    if hasattr(field.queryset.model, 'organization'):

                        if hasattr(field.queryset.model, 'is_global'):

                            self.fields[field_name].queryset = field.queryset.filter(
                                Q(organization__in=user_organizations_id)
                                |
                                Q(is_global = True)
                            )

                        else:

                            self.fields[field_name].queryset = field.queryset.filter(
                                Q(organization__in=user_organizations_id)
                            )


        if self.Meta.fields:

            if self.organization_field in self.Meta.fields:

                self.fields[self.organization_field].queryset = self.fields[self.organization_field].queryset.filter(
                    Q(id__in=user_organizations_id)
                      |
                    Q(manager=user)
                )
