import pytest
from django.test import Client

from rest_framework.reverse import reverse



class MetadataAttributesFunctional:
    """ Functional Tests for API, HTTP/Options Method
    
    These tests ensure that **ALL** serializers include the metaclass that adds the required
    data to the HTTP Options method.

    Metaclass adds data required for the UI to function correctly.
    """

    app_namespace: str = None

    url_name: str = None


    def test_method_options_request_list_ok(self):
        """Test HTTP/Options Method

        Ensure the request returns `OK`.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert response.status_code == 200


    def test_method_options_request_list_data_returned(self):
        """Test HTTP/Options Method

        Ensure the request returns data.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert response.data is not None


    def test_method_options_request_list_data_type(self):
        """Test HTTP/Options Method

        Ensure the request data returned is of type `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert type(response.data) is dict


    def test_method_options_request_list_data_has_key_table_fields(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `table_fields`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert 'table_fields' in response.data


    def test_method_options_request_list_data_key_table_fields_is_list(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert type(response.data['table_fields']) is list


    def test_method_options_request_list_data_key_table_fields_is_list_of_str(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] list is of `str`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        all_string = True

        for item in response.data['table_fields']:

            if type(item) is not str:

                all_string = False


        assert all_string


    def test_method_options_request_detail_ok(self):
        """Test HTTP/Options Method

        Ensure the request returns `OK`.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options( url, content_type='application/json' )

        assert response.status_code == 200


    def test_method_options_request_detail_data_returned(self):
        """Test HTTP/Options Method

        Ensure the request returns data.
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert response.data is not None


    def test_method_options_request_detail_data_type(self):
        """Test HTTP/Options Method

        Ensure the request data returned is of type `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data) is dict


    def test_method_options_request_detail_data_has_key_page_layout(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `layout`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert 'layout' in response.data


    def test_method_options_request_detail_data_key_page_layout_is_list(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data['layout']) is list


    def test_method_options_request_detail_data_key_page_layout_is_list_of_dict(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'] list is of `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        all_dict = True

        for item in response.data['layout']:

            if type(item) is not dict:

                all_dict = False


        assert all_dict


    def test_method_options_request_detail_data_key_page_layout_dicts_key_exists_name(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'].x has key `name`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        has_key = True

        for item in response.data['layout']:

            if 'name' not in item:

                has_key = False


        assert has_key


    def test_method_options_request_detail_data_key_page_layout_dicts_key_type_name(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'].x.[name] is of type `str`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        all_are_str = True

        for item in response.data['layout']:

            if type(item['name']) is not str:

                all_are_str = False


        assert all_are_str


    def test_method_options_request_detail_data_key_page_layout_dicts_key_exists_sections(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'].x has key `sections`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        has_key = True

        for item in response.data['layout']:

            if 'sections' not in item:

                has_key = False


        assert has_key


    def test_method_options_request_detail_data_key_page_layout_dicts_key_type_sections(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'].x.[sections] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        all_are_str = True

        for item in response.data['layout']:

            if type(item['sections']) is not list:

                all_are_str = False


        assert all_are_str



    def test_method_options_request_detail_data_has_key_urls(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `urls`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert 'urls' in response.data


    def test_method_options_request_detail_data_key_urls_is_dict(self):
        """Test HTTP/Options Method

        Ensure the request data key `urls` is dict
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data['urls']) is dict



    def test_method_options_request_detail_data_has_key_urls_self(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `urls.self`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert 'urls' in response.data


    def test_method_options_request_detail_data_key_urls_self_is_str(self):
        """Test HTTP/Options Method

        Ensure the request data key `urls.self` is a string
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-detail',
                kwargs=self.url_view_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data['urls']['self']) is str



    @pytest.mark.skip(reason='to be written')
    def test_method_options_no_field_is_generic(self):
        """Test HTTP/Options Method

        Fields are used for the UI to setup inputs correctly.

        Ensure all fields at path `.actions.<METHOD>.<name>.type` do not have `GenericField` as the value.
        """

        pass
