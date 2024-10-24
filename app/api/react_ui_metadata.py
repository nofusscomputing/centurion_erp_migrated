from rest_framework import serializers
from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.request import clone_request
from rest_framework.utils.field_mapping import ClassLookupDict

from app.serializers.user import User, UserBaseSerializer

from core.fields.badge import BadgeField
from core.fields.icon import IconField



class OverRideJSONAPIMetadata(JSONAPIMetadata):

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
            IconField: 'Icon',
            User: 'Relationship',
            UserBaseSerializer: 'Relationship'
        }
    )



class ReactUIMetadata(OverRideJSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = {}

        metadata["name"] = view.get_view_name()

        metadata["description"] = view.get_view_description()

        metadata["renders"] = [
            renderer.media_type for renderer in view.renderer_classes
        ]

        metadata["parses"] = [parser.media_type for parser in view.parser_classes]

        metadata["allowed_methods"] = view.allowed_methods

        if hasattr(view, 'get_serializer'):
            serializer = view.get_serializer()
            metadata['fields'] = self.get_serializer_info(serializer)


        if view.suffix == 'Instance':

            metadata['layout'] = view.get_page_layout()


            if hasattr(view, 'get_model_documentation'):

                if view.get_model_documentation():

                    metadata['documentation'] = view.get_model_documentation()


        elif view.suffix == 'List':

            if hasattr(view, 'table_fields'):

                metadata['table_fields'] = view.get_table_fields()

            if view.documentation:

                metadata['documentation'] = view.documentation

            if hasattr(view, 'page_layout'):

                metadata['layout'] = view.get_page_layout()


        metadata['navigation'] = [
            {
                "display_name": "Access",
                "name": "access",
                "pages": [
                    {
                        "display_name": "Organization",
                        "name": "organization",
                        "link": "/access/organization"
                    }
                ]
            },
            {
                "display_name": "Assistance",
                "name": "assistance",
                "pages": [
                    {
                        "display_name": "Requests",
                        "name": "request",
                        "icon": "ticket",
                        "link": "/assistance/ticket/request"
                    },
                    {
                        "display_name": "Knowledge Base",
                        "name": "knowledge_base",
                        "icon": "kb",
                        "link": "/assistance/knowledge_base"
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
                    },
                    {
                        "display_name": "Operating System",
                        "name": "operating_system",
                        "link": "/itam/operating_system"
                    },
                    {
                        "display_name": "Software",
                        "name": "software",
                        "link": "/itam/software"
                    }
                ]
            },
            {
                "display_name": "ITIM",
                "name": "itim",
                "pages": [
                    {
                        "display_name": "Clusters",
                        "name": "cluster",
                        "link": "/itim/cluster"
                    },
                    {
                        "display_name": "Services",
                        "name": "service",
                        "link": "/itim/service"
                    },
                ]
            },
            {
                "display_name": "Config Management",
                "name": "config_management",
                "icon": "ansible",
                "pages": [
                    {
                        "display_name": "Groups",
                        "name": "config_group",
                        "link": "/config_management/group"
                    }
                ]
            },
            {
                "display_name": "Project Management",
                "name": "project_management",
                "pages": [
                    {
                        "display_name": "Projects",
                        "name": "project",
                        "link": "/project_management/project"
                    }
                ]
            },

            {
                "display_name": "Settings",
                "name": "settings",
                "pages": [
                    {
                        "display_name": "System",
                        "name": "system",
                        "icon": "settings",
                        "link": "/settings"
                    },
                    {
                        "display_name": "Task Log",
                        "name": "celery_task_log",
                        # "icon": "settings",
                        "link": "/settings/celery_log"
                    }
                ]
            }
        ]


        return metadata
