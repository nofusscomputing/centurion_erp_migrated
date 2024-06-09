
import pytest
import unittest
import requests

from django.test import TestCase

from access.models import Organization

from core.models.history import History

from config_management.models.groups import ConfigGroups, ConfigGroupSoftware

from itam.models.device import DeviceSoftware
from itam.models.software import Software




class ConfigGroupSoftwareHistory(TestCase):

    model = ConfigGroupSoftware

    parent_model = ConfigGroups


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.parent_object = self.parent_model.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization
        )

        software = Software.objects.create(
            name = 'test_item_' + self.model._meta.model_name,
            organization = self.organization
        )

        self.item_create = self.model.objects.create(
            organization = self.organization,
            config_group = self.parent_object,
            software = software,
            action = DeviceSoftware.Actions.INSTALL,
        )


        self.history_create = History.objects.get(
            action = History.Actions.ADD[0],
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name
        )

        self.item_change = self.item_create
        self.item_change.action = DeviceSoftware.Actions.REMOVE
        self.item_change.save()

        self.history_change = History.objects.get(
            action = History.Actions.UPDATE[0],
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )

        # self.item_delete = self.item_change
        # 
        software_two = Software.objects.create(
            name = 'test_item_two_' + self.model._meta.model_name,
            organization = self.organization
        )

        self.item_delete = self.model.objects.create(
            organization = self.organization,
            config_group = self.parent_object,
            software = software_two,
            action = DeviceSoftware.Actions.INSTALL,
        )

        self.deleted_pk = self.item_delete.pk

        self.item_delete.delete()

        self.history_delete = History.objects.get(
            action = History.Actions.DELETE[0],
            item_pk = self.deleted_pk,
            item_class = self.model._meta.model_name,
        )


    def test_configgroup_software_history_entry_item_add_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_create.__dict__

        assert history['action'] == int(History.Actions.ADD[0])
        # assert type(history['action']) is int


    @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_add_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_create.__dict__

        assert history['after'] == str('{}')
        # assert type(history['after']) is str


    def test_configgroup_software_history_entry_item_add_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_create.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    def test_configgroup_software_history_entry_item_add_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_create.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    def test_configgroup_software_history_entry_item_add_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_create.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str


    def test_configgroup_software_history_entry_item_add_field_parent_pk(self):
        """ Ensure history entry field parent_pk is the created parents pk """

        history = self.history_create.__dict__

        assert history['item_parent_pk'] == self.parent_object.pk
        # assert type(history['parentpk']) is int


    def test_configgroup_software_history_entry_item_add_field_parent_class(self):
        """ Ensure history entry field parent_class is the model name """

        history = self.history_create.__dict__

        assert history['item_parent_class'] == self.parent_model._meta.model_name
        # assert type(history['item_class']) is str




################################## Change ##################################




    def test_configgroup_software_history_entry_item_change_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_change.__dict__

        assert history['action'] == int(History.Actions.UPDATE[0])
        # assert type(history['action']) is int


    def test_configgroup_software_history_entry_item_change_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_change.__dict__

        assert history['after'] == str('{"action": "' + DeviceSoftware.Actions.REMOVE + '"}')
        # assert type(history['after']) is str


    @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_change_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_change.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    def test_configgroup_software_history_entry_item_change_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_change.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    def test_configgroup_software_history_entry_item_change_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_change.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str


    def test_configgroup_software_history_entry_item_change_field_parent_pk(self):
        """ Ensure history entry field parent_pk is the created parent pk """

        history = self.history_change.__dict__

        assert history['item_parent_pk'] == self.parent_object.pk
        # assert type(history['item_pk']) is int


    def test_configgroup_software_history_entry_item_change_field_parent_class(self):
        """ Ensure history entry field parent_class is the model name """

        history = self.history_change.__dict__

        assert history['item_parent_class'] == self.parent_model._meta.model_name
        # assert type(history['item_class']) is str




################################## Delete ##################################




    def test_configgroup_software_history_entry_item_delete_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_delete.__dict__

        assert history['action'] == int(History.Actions.DELETE[0])
        # assert type(history['action']) is int


    # @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_delete.__dict__

        assert history['after'] == None
        # assert type(history['after']) is str


    # @pytest.mark.skip(reason="to be written")
    @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_delete.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    # @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_delete.__dict__

        assert history['item_pk'] == self.deleted_pk
        # assert type(history['item_pk']) is int


    # @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_delete.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str



    # @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_parent_pk(self):
        """ Ensure history entry field item_pk is the created parents pk """

        history = self.history_delete.__dict__

        assert history['item_parent_pk'] == self.parent_object.pk
        # assert type(history['item_pk']) is int


    # @pytest.mark.skip(reason="figure out best way to test")
    def test_configgroup_software_history_entry_item_delete_field_parent_class(self):
        """ Ensure history entry field parent_class is the model name """

        history = self.history_delete.__dict__

        assert history['item_parent_class'] == self.parent_model._meta.model_name
        # assert type(history['item_class']) is str



