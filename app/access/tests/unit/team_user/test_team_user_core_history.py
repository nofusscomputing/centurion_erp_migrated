
import pytest
import unittest
import requests

from django.contrib.auth.models import User
from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_child_model import HistoryEntryChildItem

from access.models import Team, TeamUsers



class TeamUsersHistory(TestCase, HistoryEntry, HistoryEntryChildItem):

    model = TeamUsers

    model_name = 'teamusers'


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item_parent = Team.objects.create(
            team_name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization
        )

        self.user = User.objects.create(
            username = 'test_item_' + self.model._meta.model_name,
            password = 'a random password'
        )

        self.item_create = self.model.objects.create(
            user = self.user,
            team = self.item_parent
        )


        self.history_create = History.objects.get(
            action = History.Actions.ADD[0],
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_change = self.item_create
        self.item_change.manager = True
        self.item_change.save()

        self.field_after_expected_value = '{"manager": true}'

        self.history_change = History.objects.get(
            action = History.Actions.UPDATE[0],
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )


        self.user_delete = User.objects.create(
            username = 'test_item_delete' + self.model._meta.model_name,
            password = 'a random password'
        )

        self.item_delete = self.model.objects.create(
            user = self.user_delete,
            team = self.item_parent
        )

        self.deleted_pk = self.item_delete.pk

        self.item_delete.delete()

        self.history_delete = History.objects.get(
            action = History.Actions.DELETE[0],
            item_pk = self.deleted_pk,
            item_class = self.model._meta.model_name,
        )

        self.history_delete_children = History.objects.filter(
            item_parent_pk = self.deleted_pk,
            item_parent_class = self.item_parent._meta.model_name,
        )
