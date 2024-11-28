import pytest
import unittest

from django.shortcuts import reverse
from django.test import TestCase, Client



class SerializerView:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """



    def test_returned_serializer_user_view(self):
        """ Check correct Serializer is returned

        View action for view user must return `ViewSerializer`
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ViewSerializer')



class SerializerAdd:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_list: str
    """ URL view name of the item list page """

    url_kwargs: dict = None
    """ URL view kwargs for the item list page """

    add_data: dict = None


    def test_returned_serializer_user_add(self):
        """ Check correct Serializer is returned

        Add action for add user must return `ModelSerializer`
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ModelSerializer')



class SerializerChange:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    change_data: dict = None


    def test_returned_serializer_user_change(self):
        """ Check correct Serializer is returned

        Change action for change user must return `ModelSerializer`
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ModelSerializer')



class SerializerDelete:


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    delete_data: dict = None


    def test_returned_serializer_user_delete(self):
        """ Check correct Serializer is returned

        Delete action for delete user must return `ModelSerializer`
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ModelSerializer')



class SerializersTestCases(
    SerializerAdd,
    SerializerChange,
    SerializerDelete,
    SerializerView
):
    """ Abstract class containing all ViewSet test cases """

    model: object
    """ Item Model to test """
