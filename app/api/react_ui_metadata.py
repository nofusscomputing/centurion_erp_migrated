import re

from django.conf import settings
from django.utils.encoding import force_str

from django.contrib.auth.models import ContentType, Permission

from rest_framework import serializers
from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.request import clone_request
from rest_framework.reverse import reverse
from rest_framework.utils.field_mapping import ClassLookupDict

from rest_framework_json_api.utils import get_related_resource_type

from access.models import Organization

from app.serializers.user import User, UserBaseSerializer

from core import fields as centurion_field
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
            UserBaseSerializer: 'Relationship',
            centurion_field.CharField: 'String',
            centurion_field.MarkdownField: 'Markdown'
        }
    )



class ReactUIMetadata(OverRideJSONAPIMetadata):


    def determine_metadata(self, request, view):

        metadata = {}

        metadata["name"] = view.get_view_name()

        metadata["description"] = view.get_view_description()

        metadata['urls']: dict = {}

        url_self = None


        if view.kwargs.get('pk', None) is not None:

            qs = view.get_queryset()[0]

            if hasattr(qs, 'get_url'):

                url_self = qs.get_url( request=request )


        elif view.kwargs:

            url_self = reverse('v2:' + view.basename + '-list', request = view.request, kwargs = view.kwargs )

        else:

            url_self = reverse('v2:' + view.basename + '-list', request = view.request )

        if url_self:

            metadata['urls'].update({'self': url_self})

        if view.get_back_url():

            metadata['urls'].update({'back': view.get_back_url()})

        if view.get_return_url():

            metadata['urls'].update({'return_url': view.get_return_url()})


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


        build_repo: str = None

        if settings.BUILD_REPO:

            build_repo = settings.BUILD_REPO

        build_sha: str = None

        if settings.BUILD_SHA:

            build_sha = settings.BUILD_SHA

        build_version: str = 'development'

        if settings.BUILD_VERSION:

            build_version = settings.BUILD_VERSION


        metadata['version']: dict = {
            'project_url': build_repo,
            'sha': build_sha,
            'version': build_version,
        }


        metadata['navigation'] = self.get_navigation(request.user)

        return metadata




    def get_field_info(self, field):
        """ Custom from `rest_framewarok_json_api.metadata.py`

        Require that read-only fields have their choices added to the 
        metadata.

        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = {}
        serializer = field.parent

        if hasattr(field, 'textarea'):

            if field.textarea:

                field_info["multi_line"] = True

        if isinstance(field, serializers.ManyRelatedField):
            field_info["type"] = self.type_lookup[field.child_relation]
        else:
            field_info["type"] = self.type_lookup[field]

        try:
            serializer_model = serializer.Meta.model
            field_info["relationship_type"] = self.relation_type_lookup[
                getattr(serializer_model, field.field_name)
            ]
        except KeyError:
            pass
        except AttributeError:
            pass
        else:
            field_info["relationship_resource"] = get_related_resource_type(field)

        if hasattr(field, 'autolink'):

            if field.autolink:

                field_info['autolink'] = field.autolink


        field_info["required"] = getattr(field, "required", False)


        if hasattr(field, 'style_class'):

            field_info["style"]: dict = {
                'class': field.style_class
            }


        attrs = [
            "read_only",
            "write_only",
            "label",
            "help_text",
            "min_length",
            "max_length",
            "min_value",
            "max_value",
            "initial",
        ]

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != "":
                field_info[attr] = force_str(value, strings_only=True)

        if getattr(field, "child", None):
            field_info["child"] = self.get_field_info(field.child)
        elif getattr(field, "fields", None):
            field_info["children"] = self.get_serializer_info(field)

        if (
            hasattr(field, "choices")
        ):
            field_info["choices"] = [
                {
                    "value": choice_value,
                    "display_name": force_str(choice_name, strings_only=True),
                }
                for choice_value, choice_name in field.choices.items()
            ]

        if (
            hasattr(serializer, "included_serializers")
            and "relationship_resource" in field_info
        ):
            field_info["allows_include"] = (
                field.field_name in serializer.included_serializers
            )


        if field_info["type"] == 'Markdown':

            linked_models = []

            linked_tickets = []

            field_info["render"] = {
                'models': {},
                'tickets': {},
            }


            if(
                field.context['view'].kwargs.get('pk', None)
                or field.context['view'].metadata_markdown
            ):

                queryset = field.context['view'].get_queryset()

                from core.lib.slash_commands.linked_model import CommandLinkedModel
                from core.models.ticket.ticket import Ticket

                for obj in queryset:

                    value = getattr(obj, field.source, None)

                    if field.source == 'display_name':

                        value = str(obj)


                    if value:

                        linked_models = re.findall(r'\s\$(?P<model_type>[a-z_]+)-(?P<model_id>\d+)[\s|\n]?', ' ' + str(value) + ' ')
                        linked_tickets = re.findall(r'(?P<ticket>#(?P<number>\d+))', str(value))

                    if(getattr(obj, 'from_ticket_id_id', None)):

                        linked_tickets += re.findall(r'(?P<ticket>#(?P<number>\d+))', '#' + str(obj.to_ticket_id_id))


                    for ticket, number in linked_tickets:

                        try:

                            item = Ticket.objects.get( pk = number )

                            field_info["render"]['tickets'].update({
                                number: {
                                    'status': Ticket.TicketStatus.All(item.status).label,
                                    'ticket_type': Ticket.TicketType(item.ticket_type).label,
                                    'title': str(item),
                                    'url': str(item.get_url()).replace('/api/v2', '')
                                }
                            })

                        except Ticket.DoesNotExist as e:

                            pass


                    for model_type, model_id in linked_models:

                        try:

                            model, item_type = CommandLinkedModel().get_model( model_type )

                            if model:

                                item = model.objects.get( pk = model_id )

                                item_meta = { 
                                    model_id: {
                                        'title': str(item),
                                        'url': str(item.get_url()).replace('/api/v2', ''),
                                    }
                                }

                                if not field_info["render"]['models'].get(model_type, None):

                                    field_info["render"]['models'].update({
                                        model_type: item_meta
                                    })

                                else:

                                    field_info["render"]['models'][model_type].update( item_meta )

                        except model.DoesNotExist as e:

                            pass


        return field_info


    _nav = {
        'access': {
            "display_name": "Access",
            "name": "access",
            "pages": {
                'view_organization': {
                    "display_name": "Organization",
                    "name": "organization",
                    "link": "/access/organization"
                }
            }
        },
        'assistance': {
            "display_name": "Assistance",
            "name": "assistance",
            "pages": {
                'core.view_ticket_request': {
                    "display_name": "Requests",
                    "name": "request",
                    "icon": "ticket_request",
                    "link": "/assistance/ticket/request"
                },
                'view_knowledgebase': {
                    "display_name": "Knowledge Base",
                    "name": "knowledge_base",
                    "icon": "information",
                    "link": "/assistance/knowledge_base"
                }
            }
        },
        'itam': {
            "display_name": "ITAM",
            "name": "itam",
            "pages": {
                'view_device': {
                    "display_name": "Devices",
                    "name": "device",
                    "icon": "device",
                    "link": "/itam/device"
                },
                'view_operatingsystem': {
                    "display_name": "Operating System",
                    "name": "operating_system",
                    "link": "/itam/operating_system"
                },
                'view_software': {
                    "display_name": "Software",
                    "name": "software",
                    "link": "/itam/software"
                }
            }
        },
        'itim': {
            "display_name": "ITIM",
            "name": "itim",
            "pages": {
                'core.view_ticket_change': {
                    "display_name": "Changes",
                    "name": "ticket_change",
                    "link": "/itim/ticket/change"
                },
                'view_cluster': {
                    "display_name": "Clusters",
                    "name": "cluster",
                    "link": "/itim/cluster"
                },
                'core.view_ticket_incident': {
                    "display_name": "Incidents",
                    "name": "ticket_incident",
                    "link": "/itim/ticket/incident"
                },
                'core.view_ticket_problem': {
                    "display_name": "Problems",
                    "name": "ticket_problem",
                    "link": "/itim/ticket/problem"
                },
                'view_service': {
                    "display_name": "Services",
                    "name": "service",
                    "link": "/itim/service"
                },
            }
        },
        'config_management': {
            "display_name": "Config Management",
            "name": "config_management",
            "icon": "ansible",
            "pages": {
                'view_configgroups': {
                    "display_name": "Groups",
                    "name": "group",
                    "icon": 'config_management',
                    "link": "/config_management/group"
                }
            }
        },
        'project_management': {
            "display_name": "Project Management",
            "name": "project_management",
            "icon": 'project',
            "pages": {
                'view_project': {
                    "display_name": "Projects",
                    "name": "project",
                    "icon": 'kanban',
                    "link": "/project_management/project"
                }
            }
        },

        'settings': {
            "display_name": "Settings",
            "name": "settings",
            "pages": {
                'all_settings': {
                    "display_name": "System",
                    "name": "setting",
                    "icon": "system",
                    "link": "/settings"
                },
                'django_celery_results.view_taskresult': {
                    "display_name": "Task Log",
                    "name": "celery_log",
                    # "icon": "settings",
                    "link": "/settings/celery_log"
                }
            }
        }
    }


    def get_navigation(self, user) -> list(dict()):
        """Render the navigation menu

        Check the users permissions agains `_nav`. if they have the permission, add the
        menu entry to the navigation to be rendered,

        **No** Menu is to be rendered that contains no menu entries.

        Args:
            user (User): User object from the request.

        Returns:
            list(dict()): Rendered navigation menu in the format the UI requires it to be.
        """

        nav: list = []

        processed_permissions: dict = {}

        for group in user.groups.all():

            for permission in group.permissions.all():

                if str(permission.codename).startswith('view_'):


                    if not processed_permissions.get(permission.content_type.app_label, None):

                        processed_permissions.update({permission.content_type.app_label: {}})

                    if permission.codename not in processed_permissions[permission.content_type.app_label]:

                        processed_permissions[permission.content_type.app_label].update({str(permission.codename): '_'})

        view_settings: list = [
            'assistance.view_knowledgebasecategory',
            'core.view_manufacturer',
            'core.view_ticketcategory',
            'core.view_ticketcommentcategory',
            'itam.view_devicemodel',
            'itam.view_devicetype',
            'itam.view_softwarecategory',
            'itim.view_clustertype',
            'project_management.view_projectstate',
            'project_management.view_projecttype',
            'settings.view_appsettings',
        ]


        # user = view.request.user

        user_orgainzations = Organization.objects.filter(
            manager = user
        )


        for app, entry in self._nav.items():

            new_menu_entry: dict = {}

            new_pages: list = []

            # if processed_permissions.get(app, None):    # doesn't cater for `.` in perm

            for permission, page in entry['pages'].items():

                if permission == 'all_settings':

                    for setting_permission in view_settings:

                        app_permission = str(setting_permission).split('.')

                        if processed_permissions.get(app_permission[0], None):

                            if processed_permissions[app_permission[0]].get(app_permission[1], None):

                                new_pages += [ page ]

                                break


                elif '.' in permission:

                    app_permission = str(permission).split('.')

                    if processed_permissions.get(app_permission[0], None):

                        if processed_permissions[app_permission[0]].get(app_permission[1], None):

                            new_pages += [ page ]

                else:

                    if processed_permissions.get(app, None):

                        if processed_permissions[app].get(permission, None):

                            new_pages += [ page ]


                if(
                    app == 'access'
                    and permission == 'view_organization'
                    and len(user_orgainzations) > 0
                ):

                    if page not in new_pages:

                        new_pages += [ page ]


            if len(new_pages) > 0:

                new_menu_entry = entry.copy()

                new_menu_entry.update({ 'pages': new_pages })

                nav += [ new_menu_entry ]

        return nav
