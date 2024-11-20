
import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_child_model import HistoryEntryChildItem

from itam.models.device import Device, DeviceOperatingSystem

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class DeviceOperatingSystemHistory(TestCase, HistoryEntry, HistoryEntryChildItem):


    model = DeviceOperatingSystem


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item_parent = Device.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_parent_two = Device.objects.create(
            name = 'test_item_two_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_operating_system = OperatingSystem.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_operating_system_version = OperatingSystemVersion.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
            operating_system = self.item_operating_system,
        )

        self.item_create = self.model.objects.create(
            organization = self.organization,
            operating_system_version = self.item_operating_system_version,
            device = self.item_parent,
        )


        self.history_create = History.objects.get(
            action = int(History.Actions.ADD),
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )


        self.item_operating_system_version_changed = OperatingSystemVersion.objects.create(
            name = 'test_item_changed_' + self.model._meta.model_name,
            organization = self.organization,
            operating_system = self.item_operating_system,
        )

        self.item_change = self.item_create
        self.item_change.operating_system_version = self.item_operating_system_version_changed
        self.item_change.save()

        self.field_after_expected_value = '{"operating_system_version_id": ' + str(self.item_operating_system_version_changed.pk) + '}'

        self.history_change = History.objects.get(
            action = int(History.Actions.UPDATE),
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )


        self.item_operating_system_delete = OperatingSystem.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_operating_system_version_delete = OperatingSystemVersion.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization,
            operating_system = self.item_operating_system,
        )

        self.item_delete = self.model.objects.create(
            operating_system_version = self.item_operating_system_version_delete,
            organization = self.organization,
            device = self.item_parent_two,
        )

        self.deleted_pk = self.item_delete.pk

        self.item_delete.delete()

        self.history_delete = History.objects.get(
            action = int(History.Actions.DELETE),
            item_pk = self.deleted_pk,
            item_class = self.model._meta.model_name,
        )

        self.history_delete_children = History.objects.filter(
            item_parent_pk = self.deleted_pk,
            item_parent_class = self.model._meta.model_name,
        )



    def test_history_entry_item_delete_field_parent_pk(self):
        """ Ensure history entry field item_pk is the created parents pk """

        history = self.history_delete.__dict__

        assert history['item_parent_pk'] == self.item_parent_two.pk
        # assert type(history['item_pk']) is int
