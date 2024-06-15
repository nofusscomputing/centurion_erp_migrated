
import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_child_model import HistoryEntryChildItem

from itam.models.device import Device, DeviceSoftware

from itam.models.software import Software, SoftwareVersion

class DeviceSoftwareHistory(TestCase, HistoryEntry, HistoryEntryChildItem):


    model = DeviceSoftware


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item_parent = Device.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_software = Software.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_software_version = SoftwareVersion.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization,
            software = self.item_software,
        )

        self.item_create = self.model.objects.create(
            installedversion = self.item_software_version,
            organization = self.organization,
            software = self.item_software,
            device = self.item_parent,
        )


        self.history_create = History.objects.get(
            action = History.Actions.ADD[0],
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )


        self.item_software_version_changed = SoftwareVersion.objects.create(
            name = 'test_item_changed' + self.model._meta.model_name,
            organization = self.organization,
            software = self.item_software,
        )

        self.item_change = self.item_create
        self.item_change.installedversion = self.item_software_version_changed
        self.item_change.save()

        self.field_after_expected_value = '{"installedversion_id": ' + str(self.item_software_version_changed.pk) + '}'

        self.history_change = History.objects.get(
            action = History.Actions.UPDATE[0],
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )


        self.item_software_delete = Software.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization,
        )

        self.item_software_version_delete = SoftwareVersion.objects.create(
            name = 'test_item_delete_' + self.model._meta.model_name,
            organization = self.organization,
            software = self.item_software,
        )

        self.item_delete = self.model.objects.create(
            installedversion = self.item_software_version_delete,
            organization = self.organization,
            software = self.item_software_delete,
            device = self.item_parent,
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
            item_parent_class = self.model._meta.model_name,
        )
