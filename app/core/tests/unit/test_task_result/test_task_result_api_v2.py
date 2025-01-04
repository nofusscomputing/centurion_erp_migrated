import pytest
import unittest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from django_celery_results.models import TaskResult

from rest_framework.relations import Hyperlink

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_fields import APICommonFields



class CeleryTaskResultAPI(
    TestCase,
    APICommonFields
):

    model = TaskResult

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

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

        self.view_user = User.objects.create_user(username="test_user_view", password="password")

        self.item = self.model.objects.create(
            task_id = 'd15233ee-a14d-4135-afe5-e406b1b61330',
            task_name = 'itam.tasks.process_inventory',
            task_args = '{"random": "value"}',
            task_kwargs = 'sdas',
            status = "SUCCESS",
            worker = "debug-itsm@laptop2",
            content_type = "application/json",
            content_encoding = "utf-8",
            result = "finished...",
            traceback = "a trace",
            meta = 'meta',
            periodic_task_name = 'a name',
        )


        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )


        self.url_view_kwargs = {'pk': self.item.id}

        client = Client()
        url = reverse('v2:_api_v2_celery_log-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data




    def test_api_field_exists_task_id(self):
        """ Test for existance of API Field

        task_id field must exist
        """

        assert 'task_id' in self.api_data


    def test_api_field_type_task_id(self):
        """ Test for type for API Field

        task_id field must be str
        """

        assert type(self.api_data['task_id']) is str




    def test_api_field_exists_periodic_task_name(self):
        """ Test for existance of API Field

        periodic_task_name field must exist
        """

        assert 'periodic_task_name' in self.api_data


    def test_api_field_type_periodic_task_name(self):
        """ Test for type for API Field

        periodic_task_name field must be str
        """

        assert type(self.api_data['periodic_task_name']) is str



    def test_api_field_exists_task_name(self):
        """ Test for existance of API Field

        task_name field must exist
        """

        assert 'task_name' in self.api_data


    def test_api_field_type_task_name(self):
        """ Test for type for API Field

        task_name field must be str
        """

        assert type(self.api_data['task_name']) is str



    def test_api_field_exists_task_args(self):
        """ Test for existance of API Field

        task_args field must exist
        """

        assert 'task_args' in self.api_data


    def test_api_field_type_task_args(self):
        """ Test for type for API Field

        task_args field must be str
        """

        assert type(self.api_data['task_args']) is str



    def test_api_field_exists_task_kwargs(self):
        """ Test for existance of API Field

        task_kwargs field must exist
        """

        assert 'task_kwargs' in self.api_data


    def test_api_field_type_task_kwargs(self):
        """ Test for type for API Field

        task_kwargs field must be str
        """

        assert type(self.api_data['task_kwargs']) is str



    def test_api_field_exists_task_kwargs(self):
        """ Test for existance of API Field

        task_kwargs field must exist
        """

        assert 'task_kwargs' in self.api_data


    def test_api_field_type_task_kwargs(self):
        """ Test for type for API Field

        task_kwargs field must be str
        """

        assert type(self.api_data['task_kwargs']) is str



    def test_api_field_exists_status(self):
        """ Test for existance of API Field

        status field must exist
        """

        assert 'status' in self.api_data


    def test_api_field_type_status(self):
        """ Test for type for API Field

        status field must be str
        """

        assert type(self.api_data['status']) is str



    def test_api_field_exists_worker(self):
        """ Test for existance of API Field

        worker field must exist
        """

        assert 'worker' in self.api_data


    def test_api_field_type_worker(self):
        """ Test for type for API Field

        worker field must be str
        """

        assert type(self.api_data['worker']) is str



    def test_api_field_exists_content_type(self):
        """ Test for existance of API Field

        content_type field must exist
        """

        assert 'content_type' in self.api_data


    def test_api_field_type_content_type(self):
        """ Test for type for API Field

        content_type field must be str
        """

        assert type(self.api_data['content_type']) is str



    def test_api_field_exists_content_encoding(self):
        """ Test for existance of API Field

        content_encoding field must exist
        """

        assert 'content_encoding' in self.api_data


    def test_api_field_type_content_encoding(self):
        """ Test for type for API Field

        content_encoding field must be str
        """

        assert type(self.api_data['content_encoding']) is str



    def test_api_field_exists_result(self):
        """ Test for existance of API Field

        result field must exist
        """

        assert 'result' in self.api_data


    def test_api_field_type_result(self):
        """ Test for type for API Field

        result field must be str
        """

        assert type(self.api_data['result']) is str



    def test_api_field_exists_date_created(self):
        """ Test for existance of API Field

        date_created field must exist
        """

        assert 'date_created' in self.api_data


    def test_api_field_type_date_created(self):
        """ Test for type for API Field

        date_created field must be str
        """

        assert type(self.api_data['date_created']) is str



    def test_api_field_exists_date_done(self):
        """ Test for existance of API Field

        date_done field must exist
        """

        assert 'date_done' in self.api_data


    def test_api_field_type_date_done(self):
        """ Test for type for API Field

        date_done field must be str
        """

        assert type(self.api_data['date_done']) is str



    def test_api_field_exists_traceback(self):
        """ Test for existance of API Field

        traceback field must exist
        """

        assert 'traceback' in self.api_data


    def test_api_field_type_traceback(self):
        """ Test for type for API Field

        traceback field must be str
        """

        assert type(self.api_data['traceback']) is str



    def test_api_field_exists_meta(self):
        """ Test for existance of API Field

        meta field must exist
        """

        assert 'meta' in self.api_data


    def test_api_field_type_meta(self):
        """ Test for type for API Field

        meta field must be str
        """

        assert type(self.api_data['meta']) is str
