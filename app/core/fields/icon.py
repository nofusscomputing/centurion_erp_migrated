from rest_framework import serializers
from rest_framework.fields import empty

from core.classes.icon import Icon



class IconField(serializers.DictField):

    source = ''

    label = ''

    def __init__(self, *, read_only=True, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):

        super().__init__(read_only=read_only, write_only=write_only,
                 required=required, default=default, initial=initial, source=source,
                 label=label, help_text=help_text, style=style,
                 error_messages=error_messages, validators=validators, allow_null=allow_null)

    def to_representation(self, icons: list([Icon])):

        a_icons: list = []
        
        for icon in icons:

            a_icons += [ icon.to_json ]

        return a_icons


    def to_internal_value(self, data):
        return Icon(data.icon,data.icon_style, data.url)
