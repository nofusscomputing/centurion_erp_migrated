import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.test import Client

from core.models.ticket.ticket import Ticket


class TicketFieldPermissionsAddUser:


    def test_field_permission_status_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field status.
        """

        field_name: str = 'status'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_priority_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field priority.
        """

        field_name: str = 'priority'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name



    def test_field_permission_assigned_users_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_users.
        """

        field_name: str = 'assigned_users'
        field_value = [1]

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_assigned_teams_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_teams.
        """

        field_name: str = 'assigned_teams'
        field_value = [1]

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_created_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field created.
        """

        field_name: str = 'created'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_date_closed_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field date_closed.
        """

        field_name: str = 'date_closed'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_external_ref_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_ref.
        """

        field_name: str = 'external_ref'
        field_value = 1

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_external_system_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_system.
        """

        field_name: str = 'external_system'
        field_value = 9999

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_opened_by_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field opened_by.
        """

        field_name: str = 'opened_by'
        field_value = 1

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_planned_start_date_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_start_date.
        """

        field_name: str = 'planned_start_date'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_planned_finish_date_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_finish_date.
        """

        field_name: str = 'planned_finish_date'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_project_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field project.
        """

        field_name: str = 'project'
        field_value = self.project.id

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_real_start_date_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_start_date.
        """

        field_name: str = 'real_start_date'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_real_finish_date_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_finish_date.
        """

        field_name: str = 'real_finish_date'
        field_value = '2024-09-08T13:19:00'

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_subscribed_users_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_users.
        """

        field_name: str = 'subscribed_users'
        field_value = [1]

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_subscribed_teams_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_teams.
        """

        field_name: str = 'subscribed_teams'
        field_value = [1]

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name


    def test_field_permission_ticket_type_add_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field ticket_type.
        """

        field_name: str = 'ticket_type'
        field_value = int(Ticket.TicketType.REQUEST.value)

        if self.ticket_type_enum == int(Ticket.TicketType.REQUEST.value):
            field_value = int(Ticket.TicketType.INCIDENT.value)

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client.force_login(self.add_user)

        data = self.add_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

        except Exception as exception:

            assert exception.code == 'cant_edit_field_' + field_name



class TicketFieldPermissionsChangeUser:


    def test_field_permission_status_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field status.
        """

        field_name: str = 'status'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_priority_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field priority.
        """

        field_name: str = 'priority'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



    def test_field_permission_assigned_users_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_users.
        """

        field_name: str = 'assigned_users'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_assigned_teams_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_teams.
        """

        field_name: str = 'assigned_teams'
        field_value = [1]

        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_created_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field created.
        """

        field_name: str = 'created'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_date_closed_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field date_closed.
        """

        field_name: str = 'date_closed'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_ref_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_ref.
        """

        field_name: str = 'external_ref'
        field_value = 1


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_system_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_system.
        """

        field_name: str = 'external_system'
        field_value = 9999


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_opened_by_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field opened_by.
        """

        field_name: str = 'opened_by'
        field_value = 2


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_planned_start_date_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_start_date.
        """

        field_name: str = 'planned_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_planned_finish_date_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_finish_date.
        """

        field_name: str = 'planned_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_project_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field project.
        """

        field_name: str = 'project'
        field_value = self.project_two.id


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_start_date_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_start_date.
        """

        field_name: str = 'real_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_finish_date_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_finish_date.
        """

        field_name: str = 'real_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_subscribed_users_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_users.
        """

        field_name: str = 'subscribed_users'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_subscribed_teams_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_teams.
        """

        field_name: str = 'subscribed_teams'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_ticket_type_change_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field ticket_type.
        """

        field_name: str = 'ticket_type'
        field_value = int(Ticket.TicketType.REQUEST.value)

        if self.ticket_type_enum == int(Ticket.TicketType.REQUEST.value):
            field_value = int(Ticket.TicketType.INCIDENT.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.change_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



class TicketFieldPermissionsImportUser:
    """Although the import use has access to edit all fields
    the import user should not allow access via the UI.
    
    These tests are to ensure this.
    """


    def test_field_permission_status_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field status.
        """

        field_name: str = 'status'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_priority_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field priority.
        """

        field_name: str = 'priority'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



    def test_field_permission_assigned_users_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_users.
        """

        field_name: str = 'assigned_users'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_assigned_teams_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_teams.
        """

        field_name: str = 'assigned_teams'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_created_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field created.
        """

        field_name: str = 'created'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_date_closed_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field date_closed.
        """

        field_name: str = 'date_closed'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_ref_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_ref.
        """

        field_name: str = 'external_ref'
        field_value = 1


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_system_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_system.
        """

        field_name: str = 'external_system'
        field_value = 9999


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_opened_by_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field opened_by.
        """

        field_name: str = 'opened_by'
        field_value = 2


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_planned_start_date_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_start_date.
        """

        field_name: str = 'planned_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_planned_finish_date_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_finish_date.
        """

        field_name: str = 'planned_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_project_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field project.
        """

        field_name: str = 'project'
        field_value = self.project.id


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_start_date_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_start_date.
        """

        field_name: str = 'real_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_finish_date_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_finish_date.
        """

        field_name: str = 'real_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_subscribed_users_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_users.
        """

        field_name: str = 'subscribed_users'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_subscribed_teams_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_teams.
        """

        field_name: str = 'subscribed_teams'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_ticket_type_import_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field ticket_type.
        """

        field_name: str = 'ticket_type'
        field_value = int(Ticket.TicketType.REQUEST.value)

        if self.ticket_type_enum == int(Ticket.TicketType.REQUEST.value):
            field_value = int(Ticket.TicketType.INCIDENT.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.import_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



class TicketFieldPermissionsTriageUser:


    def test_field_permission_status_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field status.
        """

        field_name: str = 'status'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_priority_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field priority.
        """

        field_name: str = 'priority'
        field_value = int(Ticket.TicketStatus.All.ASSIGNED.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200



    def test_field_permission_assigned_users_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_users.
        """

        field_name: str = 'assigned_users'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_assigned_teams_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field assigned_teams.
        """

        field_name: str = 'assigned_teams'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_created_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field created.
        """

        field_name: str = 'created'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_date_closed_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field date_closed.
        """

        field_name: str = 'date_closed'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_ref_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_ref.
        """

        field_name: str = 'external_ref'
        field_value = 1


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_external_system_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field external_system.
        """

        field_name: str = 'external_system'
        field_value = 9999


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_opened_by_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field opened_by.
        """

        field_name: str = 'opened_by'
        field_value = 1


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_subscribed_teams_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field subscribed_teams.
        """

        field_name: str = 'subscribed_teams'
        field_value = [1]


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_ticket_type_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field ticket_type.
        """

        field_name: str = 'ticket_type'
        field_value = int(Ticket.TicketType.REQUEST.value)

        if self.ticket_type_enum == int(Ticket.TicketType.REQUEST.value):
            field_value = int(Ticket.TicketType.INCIDENT.value)


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



class ITSMTicketFieldPermissionsTriageUser(
    TicketFieldPermissionsTriageUser
):


    def test_field_permission_project_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field project.
        """

        field_name: str = 'project'
        field_value = self.project.id


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_planned_start_date_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_start_date.
        """

        field_name: str = 'planned_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_planned_finish_date_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field planned_finish_date.
        """

        field_name: str = 'planned_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_start_date_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_start_date.
        """

        field_name: str = 'real_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"


    def test_field_permission_real_finish_date_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field real_finish_date.
        """

        field_name: str = 'real_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        try:

            response = client.post(
                url,
                data=data
            )

            assert False, 'a ValidationError exception should have been thrown'

        except ValidationError as exception:

            assert exception.code == 'cant_edit_field_' + field_name

        except Exception as exception:

            assert False, f"reason: {exception}"



class ProjectTicketFieldPermissionsTriageUser(
    TicketFieldPermissionsTriageUser
):


    def test_field_permission_project_triage_user_denied(self):
        """ Check correct permission for add 

        A standard user should not be able to edit field project.
        """

        field_name: str = 'project'
        field_value = self.project.id


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value


        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_planned_start_date_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should be able to edit field planned_start_date.
        """

        field_name: str = 'planned_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value


        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_planned_finish_date_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should be able to edit field planned_finish_date.
        """

        field_name: str = 'planned_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        
        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_real_start_date_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should be able to edit field real_start_date.
        """

        field_name: str = 'real_start_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        
        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200


    def test_field_permission_real_finish_date_triage_user_allowed(self):
        """ Check correct permission for add 

        A standard user should be able to edit field real_finish_date.
        """

        field_name: str = 'real_finish_date'
        field_value = '2024-09-08T13:19:00'


        client = Client(raise_request_exception=True)
        url = reverse(self.app_namespace + ':' + self.url_name_change, kwargs=self.url_change_kwargs)

        client.force_login(self.triage_user)

        data = self.change_data.copy()
        
        data[field_name] = field_value

        
        response = client.post(
            url,
            data=data
        )

        assert response.status_code == 200




class ITSMTicketFieldBasedPermissions(
    TicketFieldPermissionsAddUser,
    TicketFieldPermissionsChangeUser,
    TicketFieldPermissionsImportUser,
    ITSMTicketFieldPermissionsTriageUser,
):

    pass



class ProjectTicketFieldBasedPermissions(
    TicketFieldPermissionsAddUser,
    TicketFieldPermissionsChangeUser,
    TicketFieldPermissionsImportUser,
    ProjectTicketFieldPermissionsTriageUser,
):

    pass


# @pytest.mark.django_db
# @pytest.mark.parametrize("field,value,status_code", [
#     ('status', int(Ticket.TicketStatus.All.ASSIGNED.value), 'cant_edit_field_status'),
#     ('priority', int(Ticket.TicketPriority.LOW), 'cant_edit_field_priority'),
# ])
# class TestFieldEditDenied:


#     ticket_type = 'change'

#     ticket_type_enum: int = int(Ticket.TicketType.CHANGE.value)

#     app_namespace = 'ITIM'

#     url_name_view = '_ticket_change_view'

#     url_name_add = '_ticket_change_add'

#     url_name_change = '_ticket_change_change'

#     url_name_delete = '_ticket_change_delete'

#     url_delete_response = reverse('ITIM:Changes')

#     # @pytest.mark.django_db
#     # @classmethod
#     # def setUpTestData(self):
#     @pytest.mark.django_db
#     # @pytest.fixture(scope="class")
#     # def setup_class(self, db):
#     @classmethod
#     # def setUpClass(self, db):
#     def setUpTestData(self):
#         """Setup Test

#         1. Create an organization for user and item
#         . create an organization that is different to item
#         2. Create a manufacturer
#         3. create teams with each permission: view, add, change, delete
#         4. create a user per team
#         """

#         organization = Organization.objects.create(name='test_org')

#         self.organization = organization

#         different_organization = Organization.objects.create(name='test_different_organization')


#         add_permissions = Permission.objects.get(
#                 codename = 'add_' + self.model._meta.model_name + '_' + self.ticket_type,
#                 content_type = ContentType.objects.get(
#                     app_label = self.model._meta.app_label,
#                     model = self.model._meta.model_name,
#                 )
#             )

#         add_team = Team.objects.create(
#             team_name = 'add_team',
#             organization = organization,
#         )

#         add_team.permissions.set([add_permissions])


#         self.add_user = User.objects.create_user(username="test_user_add", password="password")
#         teamuser = TeamUsers.objects.create(
#             team = add_team,
#             user = self.add_user
#         )


#         self.item = self.model.objects.create(
#             organization=organization,
#             title = 'A ' + self.ticket_type + ' ticket',
#             description = 'the ticket body',
#             ticket_type = int(Ticket.TicketType.REQUEST.value),
#             opened_by = self.add_user,
#             status = int(Ticket.TicketStatus.All.NEW.value)
#         )


#         self.url_view_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

#         self.url_add_kwargs = {'ticket_type': self.ticket_type}

#         # self.add_data = {
#         #     'title': 'an add ticket',
#         #     'organization': self.organization.id,
#         #     'opened_by': self.add_user.id,
#         #     'status': int(Ticket.TicketStatus.All.NEW.value)
#         # }

#         self.add_data = {
#             'title': 'an add ticket',
#             'organization': self.organization.id,
#             'opened_by': self.add_user.id,
#         }

#         self.url_change_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

#         self.change_data = {'title': 'an change to ticket', 'organization': self.organization.id}

#         self.url_delete_kwargs = {'ticket_type': self.ticket_type, 'pk': self.item.id}

#         self.delete_data = {'title': 'a delete to ticket', 'organization': self.organization.id}


#         view_permissions = Permission.objects.get(
#                 codename = 'view_' + self.model._meta.model_name + '_' + self.ticket_type,
#                 content_type = ContentType.objects.get(
#                     app_label = self.model._meta.app_label,
#                     model = self.model._meta.model_name,
#                 )
#             )

#         view_team = Team.objects.create(
#             team_name = 'view_team',
#             organization = organization,
#         )

#         view_team.permissions.set([view_permissions])


#         change_permissions = Permission.objects.get(
#                 codename = 'change_' + self.model._meta.model_name + '_' + self.ticket_type,
#                 content_type = ContentType.objects.get(
#                     app_label = self.model._meta.app_label,
#                     model = self.model._meta.model_name,
#                 )
#             )

#         change_team = Team.objects.create(
#             team_name = 'change_team',
#             organization = organization,
#         )

#         change_team.permissions.set([change_permissions])



#         delete_permissions = Permission.objects.get(
#                 codename = 'delete_' + self.model._meta.model_name + '_' + self.ticket_type,
#                 content_type = ContentType.objects.get(
#                     app_label = self.model._meta.app_label,
#                     model = self.model._meta.model_name,
#                 )
#             )

#         delete_team = Team.objects.create(
#             team_name = 'delete_team',
#             organization = organization,
#         )

#         delete_team.permissions.set([delete_permissions])


#         self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


#         self.view_user = User.objects.create_user(username="test_user_view", password="password")
#         teamuser = TeamUsers.objects.create(
#             team = view_team,
#             user = self.view_user
#         )

#         self.change_user = User.objects.create_user(username="test_user_change", password="password")
#         teamuser = TeamUsers.objects.create(
#             team = change_team,
#             user = self.change_user
#         )

#         self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
#         teamuser = TeamUsers.objects.create(
#             team = delete_team,
#             user = self.delete_user
#         )


#         self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


#         different_organization_team = Team.objects.create(
#             team_name = 'different_organization_team',
#             organization = different_organization,
#         )

#         different_organization_team.permissions.set([
#             view_permissions,
#             add_permissions,
#             change_permissions,
#             delete_permissions,
#         ])

#         TeamUsers.objects.create(
#             team = different_organization_team,
#             user = self.different_organization_user
#         )




#     def test_model_add_has_permission_field_denied(self, field,value,status_code, db):
#         """ Check correct permission for add 

#         set status to value and attempt to create a ticket.
#         A standard user should not be able to edit field status.
#         """

#         client = Client(raise_request_exception=True)
#         url = reverse(self.app_namespace + ':' + self.url_name_add, kwargs=self.url_add_kwargs)


#         client.force_login(self.add_user)

#         data = self.add_data.copy()
        
#         data[field] =  value

#         try:

#             response = client.post(
#                 url,
#                 data=data
#             )

#         except Exception as exception:

#             assert exception.code == status_code

