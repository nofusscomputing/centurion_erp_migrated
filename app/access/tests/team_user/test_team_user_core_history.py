
import pytest
import unittest
import requests

from django.test import TestCase, Client

from access.models import Organization

from core.models.history import History

from access.models import TeamUsers


# @pytest.mark.skip(reason="to be written")
# def test_history_auth_view():
#     """ User requires Permission view_history """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_create():
#     """ History row must be added to history table on create """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_update():
#     """ History row must be added to history table on updatej """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_delete():
#     """ History row must be added to history table on delete """
#     pass



# @pytest.mark.skip(reason="to be written")
# def test_history_device_operating_system_create():
#     """ History row must be added to history table on create 
    
#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_operating_system_update():
#     """ History row must be added to history table on update
    
#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_operating_system_delete():
#     """ History row must be added to history table on delete
    
#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass



# @pytest.mark.skip(reason="to be written")
# def test_history_device_software_create():
#     """ History row must be added to history table on create

#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_software_update():
#     """ History row must be added to history table on update
    
#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass


# @pytest.mark.skip(reason="to be written")
# def test_history_device_software_delete():
#     """ History row must be added to history table on delete
    
#     Must also have populated parent_item_pk and parent_item_class columns
#     """
#     pass



@pytest.mark.skip(reason="to do")
class TeamUsersHistory(TestCase):

    model = TeamUsers

    model_name = 'teamusers'


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.item_create = self.model.objects.create(
            name = 'test_item_' + self.model_name,
            organization = self.organization
        )


        self.history_create = History.objects.get(
            action = History.Actions.ADD[0],
            item_pk = self.item_create.pk,
            item_class = self.model._meta.model_name,
        )

        self.item_change = self.item_create
        self.item_change.name = 'test_item_' + self.model_name + '_changed'
        self.item_change.save()

        self.history_change = History.objects.get(
            action = History.Actions.UPDATE[0],
            item_pk = self.item_change.pk,
            item_class = self.model._meta.model_name,
        )


    @pytest.mark.skip(reason="to do")
    # field type testing to be done as part of model testing
    def test_history_entry_item_add_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_create.__dict__

        assert history['action'] == int(History.Actions.ADD[0])
        # assert type(history['action']) is int


    @pytest.mark.skip(reason="to be written")
    def test_history_entry_item_add_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_create.__dict__

        assert history['after'] == str('{}')
        # assert type(history['after']) is str


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_add_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_create.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_add_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_create.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_add_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_create.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str




################################## Change ##################################




    @pytest.mark.skip(reason="to do")
    # field type testing to be done as part of model testing
    def test_history_entry_item_change_field_action(self):
        """ Ensure action is "add" for item creation """

        history = self.history_change.__dict__

        assert history['action'] == int(History.Actions.UPDATE[0])
        # assert type(history['action']) is int


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_change_field_after(self):
        """ Ensure after field contains correct value """

        history = self.history_change.__dict__

        assert history['after'] == str('{"name": "test_item_' + self.model_name + '_changed"}')
        # assert type(history['after']) is str


    @pytest.mark.skip(reason="to be written")
    def test_history_entry_item_change_field_before(self):
        """ Ensure before field is an empty JSON string for create """

        history = self.history_change.__dict__

        assert history['before'] == str('{}')
        # assert type(history['before']) is str


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_change_field_item_pk(self):
        """ Ensure history entry field item_pk is the created items pk """

        history = self.history_change.__dict__

        assert history['item_pk'] == self.item_create.pk
        # assert type(history['item_pk']) is int


    @pytest.mark.skip(reason="to do")
    def test_history_entry_item_change_field_item_class(self):
        """ Ensure history entry field item_class is the model name """

        history = self.history_change.__dict__

        assert history['item_class'] == self.model._meta.model_name
        # assert type(history['item_class']) is str


