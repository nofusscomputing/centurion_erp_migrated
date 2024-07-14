from django import forms
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.forms import inlineformset_factory

from app import settings

from .team_users import TeamUsersForm, TeamUsers

from access.models import Team

from core.forms.common import CommonModelForm

TeamUserFormSet = inlineformset_factory(
    model=TeamUsers,
    parent_model= Team,
    extra = 1,
    fields=[
        'user',
        'manager'
    ]
)



class TeamFormAdd(CommonModelForm):

    class Meta:
        model = Team
        fields = [
            'team_name',
            'model_notes',
        ]



class TeamForm(CommonModelForm):

    class Meta:
        model = Team
        fields = [
            'team_name',
            'permissions',
            'model_notes',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created'] = forms.DateTimeField(
            label="Created",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].created,
            disabled=True,
            required=False,
        )

        self.fields['modified'] = forms.DateTimeField(
            label="Modified",
            input_formats=settings.DATETIME_FORMAT,
            initial=kwargs['instance'].modified,
            disabled=True,
            required=False,
        )

        self.fields['permissions'].widget.attrs = {'style': "height: 200px;"}

        apps = [
            'access',
            'config_management',
            'core',
            'django_celery_results',
            'itam',
            'settings',
        ]

        exclude_models = [
            'appsettings',
            'chordcounter',
            'groupresult',
            'organization'
            'settings',
            'usersettings',
        ]

        exclude_permissions = [
            'add_organization',
            'add_taskresult',
            'change_organization',
            'change_taskresult',
            'delete_organization',
            'delete_taskresult',
        ]

        self.fields['permissions'].queryset = Permission.objects.filter(
            content_type__app_label__in=apps,
        ).exclude(
            content_type__model__in=exclude_models
        ).exclude(
            codename__in = exclude_permissions
        )
