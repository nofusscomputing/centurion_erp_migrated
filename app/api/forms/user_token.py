import datetime
from django import forms

from api.models.tokens import AuthToken

from app import settings

from core.forms.common import CommonModelForm


class AuthTokenForm(CommonModelForm):

    prefix = 'user_token'

    class Meta:

        fields = [
            'note',
            'expires',
        ]

        model = AuthToken


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['expires'].widget = forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'format': "%Y-%m-%dT%H:%M"})
        self.fields['expires'].input_formats = settings.DATETIME_FORMAT
        self.fields['expires'].format="%Y-%m-%dT%H:%M"
        self.fields['expires'].initial= datetime.datetime.now() + datetime.timedelta(days=90)

        if self.prefix + '-gen_token' not in self.data:

            generated_token = self.instance.generate()

        else:

            generated_token = self.data[self.prefix + '-gen_token']

        self.fields['gen_token'] = forms.CharField(
            label="Generated Token",
            initial=generated_token,
            empty_value= generated_token,
            required=False,
            help_text = 'Ensure you save this token somewhere as you will never be able to obtain it again',
        )

        self.fields['gen_token'].widget.attrs['readonly'] = True
