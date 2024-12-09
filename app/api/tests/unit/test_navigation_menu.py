from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.react_ui_metadata import ReactUIMetadata


class NavigationMenu(
    TestCase
):


    @classmethod
    def setUpTestData(self):
        
        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        users_to_create: dict = {
            'access': [
                {
                    'content_model': 'organization',
                    'permission_model': 'organization'
                }
            ],
            'assistance': [
                {
                    'content_model': 'knowledgebase',
                    'permission_model': 'knowledgebase'
                },
                {
                    'content_model': 'knowledgebasecategory',
                    'permission_model': 'knowledgebasecategory'
                }
            ],
            'config_management': [
                {
                    'content_model': 'configgroups',
                    'permission_model': 'configgroups'
                }
            ],
            'core': [
                {
                    'content_model': 'manufacturer',
                    'permission_model': 'manufacturer'
                },
                {
                    'content_model': 'ticket',
                    'permission_model': 'ticket_change'
                },
                {
                    'content_model': 'ticket',
                    'permission_model': 'ticket_incident'
                },
                {
                    'content_model': 'ticket',
                    'permission_model': 'ticket_problem'
                },
                {
                    'content_model': 'ticket',
                    'permission_model': 'ticket_request'
                },
                {
                    'content_model': 'ticketcategory',
                    'permission_model': 'ticketcategory'
                },
                {
                    'content_model': 'ticketcommentcategory',
                    'permission_model': 'ticketcommentcategory'
                }
            ],
            'django_celery_results': [
                {
                    'content_model': 'taskresult',
                    'permission_model': 'taskresult'
                }
            ],
            'itam': [
                {
                    'content_model': 'device',
                    'permission_model': 'device'
                },
                {
                    'content_model': 'devicemodel',
                    'permission_model': 'devicemodel'
                },
                {
                    'content_model': 'devicetype',
                    'permission_model': 'devicetype'
                },
                {
                    'content_model': 'operatingsystem',
                    'permission_model': 'operatingsystem'
                },
                {
                    'content_model': 'software',
                    'permission_model': 'software'
                },
                {
                    'content_model': 'softwarecategory',
                    'permission_model': 'softwarecategory'
                }
            ],
            'itim': [
                {
                    'content_model': 'cluster',
                    'permission_model': 'cluster'
                },
                {
                    'content_model': 'clustertype',
                    'permission_model': 'clustertype'
                },
                {
                    'content_model': 'service',
                    'permission_model': 'service'
                }
            ],
            'project_management': [
                {
                    'content_model': 'project',
                    'permission_model': 'project'
                },
                {
                    'content_model': 'projectstate',
                    'permission_model': 'projectstate'
                },
                {
                    'content_model': 'projecttype',
                    'permission_model': 'projecttype'
                }
            ],
            'settings': [
                {
                    'content_model': 'appsettings',
                    'permission_model': 'appsettings'
                }
            ]
        }


        # app_label = 'access'
        # model_name = 'organization'

        for app_label, model_names in users_to_create.items():

            for model_name in model_names:

                setattr(self, app_label + "_" + model_name['permission_model'], User.objects.create_user(username= app_label + "_" + model_name['permission_model'], password="password"))

                team = Team.objects.create(
                    team_name = app_label + "_" + model_name['permission_model'],
                    organization = organization,
                )

                permission = Permission.objects.get(
                        codename = 'view_' + model_name['permission_model'],
                        content_type = ContentType.objects.get(
                            app_label = app_label,
                            model = model_name['content_model'],
                        )
                    )

                team.permissions.set( [ permission ] )

                team_user = TeamUsers.objects.create(
                    team = team,
                    user = getattr(self, app_label + "_" + model_name['permission_model'])
                )

        self.metadata = ReactUIMetadata()




    def test_navigation_menu_visible_access_organization_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.access_organization)

        menu_name = 'access'

        page_name = 'organization'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_access_organization_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.access_organization)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_config_management_configgroups_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.config_management_configgroups)

        menu_name = 'config_management'

        page_name = 'group'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_config_management_configgroups_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.config_management_configgroups)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_assistance_knowledgebase_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.assistance_knowledgebase)

        menu_name = 'assistance'

        page_name = 'knowledge_base'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_assistance_knowledgebase_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.assistance_knowledgebase)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_assistance_request_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_request)

        menu_name = 'assistance'

        page_name = 'request'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_assistance_request_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_request)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_django_celery_results_taskresult_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.django_celery_results_taskresult)

        menu_name = 'settings'

        page_name = 'celery_log'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_django_celery_results_taskresult_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.django_celery_results_taskresult)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_device_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_device)

        menu_name = 'itam'

        page_name = 'device'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_device_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_device)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_operating_system_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_operatingsystem)

        menu_name = 'itam'

        page_name = 'operating_system'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_operating_system_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_operatingsystem)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_software_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_software)

        menu_name = 'itam'

        page_name = 'software'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_software_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_software)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_cluster_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itim_cluster)

        menu_name = 'itim'

        page_name = 'cluster'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_cluster_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itim_cluster)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_ticket_change_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_change)

        menu_name = 'itim'

        page_name = 'ticket_change'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_ticket_change_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_change)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_ticket_incident_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_incident)

        menu_name = 'itim'

        page_name = 'ticket_incident'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_ticket_incident_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_incident)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_ticket_problem_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_problem)

        menu_name = 'itim'

        page_name = 'ticket_problem'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_ticket_problem_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticket_problem)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_service_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itim_service)

        menu_name = 'itim'

        page_name = 'service'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_service_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itim_service)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_project_management_project_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.project_management_project)

        menu_name = 'project_management'

        page_name = 'project'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_project_management_project_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.project_management_project)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1











    def test_navigation_menu_visible_settings_appsettings_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.settings_appsettings)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_settings_appsettings_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.settings_appsettings)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itim_clustertype_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itim_clustertype)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itim_clustertype_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itim_clustertype)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_devicemodel_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_devicemodel)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_devicemodel_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_devicemodel)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_devicetype_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_devicetype)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_devicetype_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_devicetype)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_assistance_knowledgebasecategory_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.assistance_knowledgebasecategory)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_assistance_knowledgebasecategory_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.assistance_knowledgebasecategory)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_core_manufacturer_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_manufacturer)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_core_manufacturer_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_manufacturer)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_project_management_projectstate_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.project_management_projectstate)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_project_management_projectstate_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.project_management_projectstate)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_project_management_projecttype_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.project_management_projecttype)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_project_management_projecttype_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.project_management_projecttype)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_itam_softwarecategory_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.itam_softwarecategory)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_itam_softwarecategory_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.itam_softwarecategory)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_core_ticketcategory_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticketcategory)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_core_ticketcategory_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticketcategory)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1



    def test_navigation_menu_visible_core_ticketcommentcategory_exist(self):
        """Navigation Menu Check

        Ensure that if the user has the permission, the navigation menu and
        page is available for the user
        """

        nav_menu = self.metadata.get_navigation(self.core_ticketcommentcategory)

        menu_name = 'settings'

        page_name = 'setting'

        menu_page_exists: bool = False


        for menu in nav_menu:

            for page in menu['pages']:

                if(
                    menu['name'] == menu_name
                    and page['name'] == page_name
                ):

                    menu_page_exists = True


        assert menu_page_exists



    def test_navigation_menu_visible_core_ticketcommentcategory_no_additional_exist(self):
        """Navigation Menu Check

        Ensure that only the navigation menu and entry is the only one displayed
        for the user who has the desired permission
        """

        nav_menu = self.metadata.get_navigation(self.core_ticketcommentcategory)

        pages_found: int = 0


        for menu in nav_menu:

            for page in menu['pages']:

                pages_found += 1


        assert pages_found == 1
