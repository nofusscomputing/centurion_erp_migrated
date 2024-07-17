import re

from app.urls import urlpatterns

from django.conf import settings
from django.urls import URLPattern, URLResolver

from access.models import Organization

from settings.models.user_settings import UserSettings


def build_details(context) -> dict:

    return {
        'project_url': settings.BUILD_REPO,
        'sha': settings.BUILD_SHA,
        'version': settings.BUILD_VERSION,
    }


def request(request):
    return request.get_full_path()


def social_backends(request):
    """ Fetch Backend Names

    Required for use on the login page to dynamically build the social auth URLS

    Returns:
        list(str): backend name
    """
    from importlib import import_module

    social_backends = []

    if hasattr(settings, 'SSO_BACKENDS'):

        for backend in settings.SSO_BACKENDS:

            paths = str(backend).split('.')

            module = import_module(paths[0] + '.' + paths[1] + '.' + paths[2])

            backend_class = getattr(module, paths[3])
            backend = backend_class.name

            social_backends += [ str(backend) ]

    return social_backends


def user_settings(context) -> int:
    """ Provides the settings ID for the current user.

    If user settings object doesn't exist, it's probably a new user. So create their settings row.

    Returns:
        int: model usersettings Primary Key
    """
    if context.user.is_authenticated:

        settings = UserSettings.objects.filter(user=context.user)

        if not settings.exists():

            UserSettings.objects.create(user=context.user)

            settings = UserSettings.objects.filter(user=context.user)

        return settings[0].pk

    return None


def user_default_organization(context) -> int:
    """ Provides the users default organization.

    Returns:
        int: Users Default Organization
    """
    if context.user.is_authenticated:

        settings = UserSettings.objects.filter(user=context.user)

        if settings[0].default_organization:

            return settings[0].default_organization.id

    return None


def nav_items(context) -> list(dict()):
    """ Fetch All Project URLs

    Collect the project URLs for use in creating the site navigation.

    The returned list contains a dictionary with the following items:
        name: {str} Group Name
        urls: {list} List of URLs for the group
        is_active: {bool} if any of the links in this group are active

    Each group url list item contains a dicionary with the following items:
        name: {str} The display name for the link
        url: {str} link URL
        is_active: {bool} if this link is the active URL

    Returns:
        list: Items user has view access to
    """

    dnav = []
    re_pattern = re.compile('[a-z/0-9]+')
    
    for nav_group in urlpatterns:

        group_active = False

        ignored_apps = [
            'admin',
            'djdt',     # Debug application
            'api',
            'social',
        ] 

        nav_items = []

        if (
            isinstance(nav_group, URLPattern)
        ):

            group_name = str(nav_group.name)

        elif (
            isinstance(nav_group, URLResolver)
        ):

            if nav_group.app_name is not None and str(nav_group.app_name).lower() not in ignored_apps:

                group_name = str(nav_group.app_name)

                for pattern in nav_group.url_patterns:

                    is_active = False

                    url = '/' + str(nav_group.pattern) + str(pattern.pattern)

                    if str(context.path).startswith(url):

                        is_active = True
                    
                    if str(context.path).startswith('/' + str(nav_group.pattern)):
                        group_active = True

                    if (
                        pattern.pattern.name is not None
                          and
                        not str(pattern.pattern.name).startswith('_')
                    ):

                        name = str(pattern.name)

                        if hasattr(pattern.callback.view_class, 'permission_required'):

                            permissions_required = pattern.callback.view_class.permission_required

                            user_has_perm = False

                            if type(permissions_required) is list:

                                user_has_perm = context.user.has_perms(permissions_required)

                            else:

                                user_has_perm = context.user.has_perm(permissions_required)

                            if hasattr(pattern.callback.view_class, 'model'):

                                if pattern.callback.view_class.model is Organization and context.user.is_authenticated:

                                    organizations = Organization.objects.filter(manager = context.user)

                                    if len(organizations) > 0:

                                        user_has_perm = True

                            if str(nav_group.app_name).lower() == 'settings':

                                user_has_perm = True

                            if context.user.is_superuser:

                                user_has_perm = True

                            if user_has_perm:

                                nav_items = nav_items + [ {
                                    'name': name,
                                    'url': url,
                                    'is_active': is_active
                                    } ]

        if len(nav_items) > 0:

            dnav = dnav + [{
                'name': group_name,
                'urls': nav_items,
                'is_active': group_active
                }]


    return dnav


def common(context):

    return {
        'build_details': build_details(context),
        'nav_items': nav_items(context),
        'social_backends': social_backends(context),
        'user_settings': user_settings(context),
        'user_default_organization': user_default_organization(context)
    }
