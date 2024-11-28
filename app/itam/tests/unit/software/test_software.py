import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from app.tests.abstract.models import TenancyModel

from itam.models.software import Software



class SoftwareModel(
    TestCase,
    TenancyModel
):

    model = Software


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

        self.item = self.model.objects.create(
            organization=organization,
            name = 'software'
        )


    @pytest.mark.skip(reason="to be written")
    def test_software_must_have_organization(self):
        """ Software must have organization set """
        pass

    @pytest.mark.skip(reason="to be written")
    def test_software_update_is_global_no_change(self):
        """Once software is set to global it can't be changed.

            global status can't be changed as non-global items may reference the item.
        """

        pass

    @pytest.mark.skip(reason="to be written")
    def test_software_prevent_delete_if_used(self):
        """Any software in use by a software must not be deleted.

            i.e. A software has an action set for the software.
        """

        pass
