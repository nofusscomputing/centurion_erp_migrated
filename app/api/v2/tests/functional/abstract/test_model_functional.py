from django.test import Client

from rest_framework.reverse import reverse



class ModelAttributesFunctional:
    """ Functional Tests for API, HTTP/Options Method
    
    These tests ensure that **ALL** serializers include the metaclass that addes the required
    data to the HTTP Options method.

    Metaclass adds data required for the UI to function correctly.

    This test suite depends upon Unit Test `ModelAttributesUnit` passing.
    """


    reverse_url:str = 'API:_api_v2_organization'

    model = None
    """Model to Test"""

    # model_name = 'organization'
    # app_label = 'access'


    @classmethod
    def setUpTestData(self):

        self.view_user = User.objects.create_user(username="test_user_view", password="password", is_superuser=True)

        self.item = self.model.objects.create(name='test_org', manager=self.view_user)


    def test_method_options_request_list_ok(self):
        """Test HTTP/Options Method

        Ensure the request returns `OK`.
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

        assert response.status_code == 200


    def test_method_options_request_list_data_returned(self):
        """Test HTTP/Options Method

        Ensure the request returns data.
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

        assert response.data is not None


    def test_method_options_request_list_data_type(self):
        """Test HTTP/Options Method

        Ensure the request data returned is of type `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

        assert type(response.data) is dict


    def test_method_options_request_list_data_has_key_table_fields(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `table_fields`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

        assert 'table_fields' in response.data


    def test_method_options_request_list_data_key_table_fields_is_list(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

        assert type(response.data['table_fields']) is list


    def test_method_options_request_list_data_key_table_fields_is_list_of_str(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] list is of `str`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-list'), content_type='application/json')

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

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json')

        assert response.status_code == 200


    def test_method_options_request_detail_data_returned(self):
        """Test HTTP/Options Method

        Ensure the request returns data.
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

        assert response.data is not None


    def test_method_options_request_detail_data_type(self):
        """Test HTTP/Options Method

        Ensure the request data returned is of type `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

        assert type(response.data) is dict


    def test_method_options_request_detail_data_has_key_page_layout(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `layout`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

        assert 'layout' in response.data


    def test_method_options_request_detail_data_key_page_layout_is_list(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

        assert type(response.data['layout']) is list


    def test_method_options_request_detail_data_key_page_layout_is_list_of_dict(self):
        """Test HTTP/Options Method

        Ensure the request data['layout'] list is of `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

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

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

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

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

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

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

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

        response = client.options(reverse(self.reverse_url + '-detail', kwargs={'pk': self.item.id}), content_type='application/json', kwargs={'pk': self.item.id})

        all_are_str = True

        for item in response.data['layout']:

            if type(item['sections']) is not list:

                all_are_str = False


        assert all_are_str


    @pytest.mark.skip(reason='to be written')
    def test_method_options_no_field_is_generic(self):
        """Test HTTP/Options Method

        Fields are used for the UI to setup inputs correctly.

        Ensure all fields at path `.actions.<METHOD>.<name>.type` do not have `GenericField` as the value.
        """

        pass
