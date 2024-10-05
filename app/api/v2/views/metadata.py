from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict

from core.fields.badge import BadgeField
from core.fields.icon import IconField



class OverRidesJSONAPIMetadata(JSONAPIMetadata):

    type_lookup = ClassLookupDict(
        {
            serializers.Field: "GenericField",
            serializers.RelatedField: "Relationship",
            serializers.BooleanField: "Boolean",
            serializers.CharField: "String",
            serializers.URLField: "URL",
            serializers.EmailField: "Email",
            serializers.RegexField: "Regex",
            serializers.SlugField: "Slug",
            serializers.IntegerField: "Integer",
            serializers.FloatField: "Float",
            serializers.DecimalField: "Decimal",
            serializers.DateField: "Date",
            serializers.DateTimeField: "DateTime",
            serializers.TimeField: "Time",
            serializers.ChoiceField: "Choice",
            serializers.MultipleChoiceField: "MultipleChoice",
            serializers.FileField: "File",
            serializers.ImageField: "Image",
            serializers.ListField: "List",
            serializers.DictField: "Dict",
            serializers.Serializer: "Serializer",
            serializers.JSONField: "JSON",    # New. Does not exist in base class
            BadgeField: 'Badge',
            IconField: 'Icon'
        }
    )



class NavigationMetadata(OverRidesJSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = super().determine_metadata(request, view)

        if hasattr(view, 'queryset'):

            if view.suffix == 'Instance':

                if hasattr(view.queryset.model, 'page_layout'):
                    metadata['layout'] = view.queryset.model.page_layout

                metadata['actions']['PUT'] = self.field_choices(metadata['actions']['PUT'])

                # for field_name, value in metadata['actions']['PUT'].items():

                #     if metadata['actions']['PUT'][field_name]['type'] == 'Relationship':

                #         choices = []

                #         if metadata['actions']['PUT'][field_name]['relationship_resource'] == 'DeviceType':

                #             from itam.models.device import DeviceType

                #             queryset = DeviceType.objects.filter()

                #             for item in queryset:

                #                 choices += [{
                #                     'value': item.id,
                #                     'display_name': item.name
                #                 }]

                #         metadata['actions']['PUT'][field_name].update({'choices': choices})


            elif view.suffix == 'List':

                metadata['table_fields'] = view.queryset.model.table_fields


                metadata['actions']['POST'] = self.field_choices(metadata['actions']['POST'])



            

        else:

            metadata['navigation'] = [
                {
                    "display_name": "Access",
                    "name": "access",
                    "pages": [
                        {
                            "display_name": "Organization",
                            "name": "organization",
                            "icon": "device",
                            "link": "/access/organization"
                        }
                    ]
                },
                {
                    "display_name": "ITAM",
                    "name": "itam",
                    "pages": [
                        {
                            "display_name": "Devices",
                            "name": "device",
                            "icon": "device",
                            "link": "/itam/device"
                        }
                    ]
                },

                # {
                #     "name": "Settings",
                #     "pages": [
                #         {
                #             "name": "Device Models",
                #             "icon": "device",
                #             "link": "/settings/device_model"
                #         }
                #     ]
                # }
            ]



        return metadata


    def field_choices(self, fields) -> dict:

        field_choices = fields


        for field_name, value in fields.items():

            if fields[field_name]['type'] == 'Relationship':

                choices = []

                model = None


                if fields[field_name]['relationship_resource'] == 'Device':

                    from itam.models.device import Device as model

                elif fields[field_name]['relationship_resource'] == 'DeviceModel':

                    from itam.models.device import DeviceModel as model

                elif fields[field_name]['relationship_resource'] == 'DeviceType':

                    from itam.models.device import DeviceType as model

                elif fields[field_name]['relationship_resource'] == 'Organization':

                    from access.models import Organization as model

                elif fields[field_name]['relationship_resource'] == 'Software':

                    from itam.models.software import Software as model

                elif fields[field_name]['relationship_resource'] == 'SoftwareVersion':

                    from itam.models.software import SoftwareVersion as model

                elif fields[field_name]['relationship_resource'] == 'User':

                    from django.contrib.auth.models import User as model

                if model:

                    queryset = model.objects.filter()

                    for item in queryset:

                        choices += [{
                            'value': item.id,
                            'display_name': str(item)
                        }]

                    field_choices[field_name].update({'choices': choices})


        return field_choices
