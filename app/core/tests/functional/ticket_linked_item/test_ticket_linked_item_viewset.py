from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import (
    APIPermissionAdd,
    APIPermissionChange,
    APIPermissionDelete,
    APIPermissionView
)
from api.tests.abstract.api_serializer_viewset import (
    SerializerAdd,
    SerializerDelete,
    SerializerView
)

from core.models.ticket.ticket_linked_items import Ticket, TicketLinkedItem

from settings.models.user_settings import UserSettings



class ViewSetBase:
    """ Test Cases common to ALL ticket types """

    model = TicketLinkedItem

    app_namespace = 'v2'
    
    delete_data = {}

    ticket_type: str = 'request'

    ticket_type_enum = Ticket.TicketType.REQUEST

    url_name = '_api_v2_ticket_linked_item'

    @classmethod
    def CreateOrg(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        # different_organization = Organization.objects.create(name='test_different_organization')


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        

        # organization = Organization.objects.create(name='test_org')

        # self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = self.organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = self.organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = self.organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.ticket = Ticket.objects.create(
            organization = self.organization,
            title = 'one',
            description = 'some text for body',
            opened_by = self.view_user,
            ticket_type = self.ticket_type_enum,
            status = Ticket.TicketStatus.All.NEW
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            item = self.linked_item.id,
            item_type = self.item_type,
            ticket = self.ticket,
        )


        # self.url_kwargs = {'ticket_id': self.ticket.id}

        # self.url_view_kwargs = {'ticket_id': self.ticket.id, 'pk': self.item.id}

        self.add_data = {
            'organization': self.organization.id,
            'ticket': self.ticket.id,
            'item': self.linked_item_two.id,
            'item_type': int(TicketLinkedItem.Modules.DEVICE),
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        user_settings = UserSettings.objects.get(user=self.add_user)

        user_settings.default_organization = self.organization

        user_settings.save()


        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )










class ViewSetBasePermissionsAPI(
    ViewSetBase,
    APIPermissionAdd,
    APIPermissionDelete,
    APIPermissionView,
):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass





class ViewSetBaseSerializer(
    ViewSetBase,
    SerializerAdd,
    SerializerDelete,
    SerializerView,
):

    pass



class BaseItemTicket(
    # ViewSetBasePermissionsAPI,
):
    """ Test Cases common to ALL ticket types """

    model = TicketLinkedItem

    app_namespace = 'v2'
    
    delete_data = {}

    ticket_type: str = 'request'

    ticket_type_enum = Ticket.TicketType.REQUEST

    url_name = '_api_v2_item_tickets'

    item_class: str = None

    item_type = None

    @classmethod
    def setUpTestData(self):

        from itam.models.device import Device

        super().setUpTestData()

        self.url_kwargs = {'item_class': self.item_class, 'item_id': self.linked_item.id}

        self.url_view_kwargs = {'item_class': self.item_class, 'item_id': self.linked_item.id, 'pk': self.item.id}



class BaseItemTicketPermissionsAPI(
    BaseItemTicket,
    ViewSetBasePermissionsAPI,
):



    def test_add_has_permission(self):
        """ Check correct permission for add 

        Add not allowed from this endpoint
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 201


    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as a ticket linked item obtains it's
        organization from the ticket.
        """

        pass



class BaseItemTicketSerializer(
    BaseItemTicket,
    ViewSetBaseSerializer,
):

    pass



class ItemCluster:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'cluster'

    item_type =  TicketLinkedItem.Modules.CLUSTER


    @classmethod
    def setUpTestData(self):

        from itim.models.clusters import Cluster

        self.CreateOrg()

        self.linked_item = Cluster.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = Cluster.objects.create(
            organization = self.organization,
            name = 'two',
        )


        super().setUpTestData()



class ItemClusterTicketPermissionsAPI(
    ItemCluster,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemClusterTicketSerializer(
    ItemCluster,
    BaseItemTicketSerializer,
    TestCase
):

    pass



class ItemConfigGroups:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'config_group'

    item_type =  TicketLinkedItem.Modules.CONFIG_GROUP


    @classmethod
    def setUpTestData(self):

        from config_management.models.groups import ConfigGroups

        self.CreateOrg()

        self.linked_item = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'two',
        )


        super().setUpTestData()



class ItemConfigGroupsTicketPermissionsAPI(
    ItemConfigGroups,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemConfigGroupsTicketSerializer(
    ItemConfigGroups,
    BaseItemTicketSerializer,
    TestCase
):

    pass



class ItemDeviceTicket:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'device'

    item_type =  TicketLinkedItem.Modules.DEVICE


    @classmethod
    def setUpTestData(self):

        from itam.models.device import Device

        self.CreateOrg()

        self.linked_item = Device.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = Device.objects.create(
            organization = self.organization,
            name = 'two',
        )

        super().setUpTestData()



class ItemDeviceTicketPermissionsAPI(
    ItemDeviceTicket,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemDeviceTicketSerializer(
    ItemDeviceTicket,
    BaseItemTicketSerializer,
    TestCase
):

    pass



class ItemKBTicket:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'knowledge_base'

    item_type =  TicketLinkedItem.Modules.KB


    @classmethod
    def setUpTestData(self):

        from assistance.models.knowledge_base import KnowledgeBase

        self.CreateOrg()

        self.user_one = User.objects.create_user(username="user_one", password="password")

        self.user_two = User.objects.create_user(username="user_two", password="password")

        self.linked_item = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'one',
            content = 'sadsadsads',
            target_user = self.user_one,
            responsible_user = self.user_two
        )


        self.linked_item_two = KnowledgeBase.objects.create(
            organization = self.organization,
            title = 'two',
            content = 'sadsadsads',
            target_user = self.user_two,
            responsible_user = self.user_one
        )

        super().setUpTestData()



class ItemKBTicketPermissionsAPI(
    ItemKBTicket,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemKBTicketSerializer(
    ItemKBTicket,
    BaseItemTicketSerializer,
    TestCase
):

    pass












class ItemOperatingSystem:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'operating_system'

    item_type =  TicketLinkedItem.Modules.OPERATING_SYSTEM


    @classmethod
    def setUpTestData(self):

        from itam.models.operating_system import OperatingSystem

        self.CreateOrg()

        self.linked_item = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'two',
        )


        super().setUpTestData()



class ItemOperatingSystemTicketPermissionsAPI(
    ItemOperatingSystem,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemOperatingSystemSerializer(
    ItemOperatingSystem,
    BaseItemTicketSerializer,
    TestCase
):

    pass



class ItemService:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'service'

    item_type =  TicketLinkedItem.Modules.SERVICE


    @classmethod
    def setUpTestData(self):

        from itim.models.services import Service

        self.CreateOrg()

        self.linked_item = Service.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = Service.objects.create(
            organization = self.organization,
            name = 'two',
        )


        super().setUpTestData()



class ItemServiceTicketPermissionsAPI(
    ItemService,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemServiceTicketSerializer(
    ItemService,
    BaseItemTicketSerializer,
    TestCase
):

    pass



class ItemSoftware:
    """ Test Cases common to ALL ticket types """


    item_class: str = 'software'

    item_type =  TicketLinkedItem.Modules.SOFTWARE


    @classmethod
    def setUpTestData(self):

        from itam.models.software import Software

        self.CreateOrg()

        self.linked_item = Software.objects.create(
            organization = self.organization,
            name = 'one',
        )


        self.linked_item_two = Software.objects.create(
            organization = self.organization,
            name = 'two',
        )


        super().setUpTestData()



class ItemSoftwareTicketPermissionsAPI(
    ItemSoftware,
    BaseItemTicketPermissionsAPI,
    TestCase
):

    pass



class ItemSoftwareTicketSerializer(
    ItemSoftware,
    BaseItemTicketSerializer,
    TestCase
):

    pass
