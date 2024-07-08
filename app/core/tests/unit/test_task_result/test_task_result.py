import pytest
import unittest
import requests

from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import TestCase

from celery import states

from access.models import Organization, Team, TeamUsers, Permission

from app.tests.abstract.model_permissions import ModelPermissionsView

from django_celery_results.models import TaskResult



class TaskResultPermissions(TestCase, ModelPermissionsView):


    model = TaskResult

    app_label = 'django_celery_results'

    app_namespace = 'Settings'

    url_name_view = '_task_result_view'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.item = self.model.objects.create(
            task_id='organization',
            periodic_task_name='',
            task_name = 'deviceone',
            status=states.SUCCESS,
            content_type='application/json',
            content_encoding='utf-8',
        )


        self.url_view_kwargs = {'pk': self.item.id}

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])

        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )


    def test_model_view_different_organizaiton_denied(self): # Test is N/A
        pass
