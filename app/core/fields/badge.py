from rest_framework import serializers
from rest_framework.fields import empty

from core.classes.badge import Badge

from core.fields.icon import Icon, IconField

class BadgeField(serializers.Field):

    source = ''
    label = ''
    fred = 'dsfdsfds'
    # read_only = True

    def __init__(self, *, read_only=True, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):

        super().__init__(read_only=read_only, write_only=write_only,
                 required=required, default=default, initial=initial, source=source,
                 label=label, help_text=help_text, style=style,
                 error_messages=error_messages, validators=validators, allow_null=allow_null)

        a = 'a'

    def to_representation(self, badge: Badge):
        return badge.to_json
        # return {
        #     'icon': badge.icon.to_json,
        #     'text': badge.text,
        #     'text_style': badge.text_style,
        #     'url': badge.url,
        # }

    def to_internal_value(self, data):
        return Badge(data.icon,data.colour, data.url)
