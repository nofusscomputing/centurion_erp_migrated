from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict



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
            serializers.JSONField: "JSON"    # New. Does not exist in base class
        }
    )



class NavigationMetadata(OverRidesJSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = super().determine_metadata(request, view)

        if hasattr(view, 'queryset'):

            if view.suffix == 'Instance':

                metadata['layout'] = view.queryset.model.page_layout

            elif view.suffix == 'List':

                metadata['table_fields'] = view.queryset.model.table_fields

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
