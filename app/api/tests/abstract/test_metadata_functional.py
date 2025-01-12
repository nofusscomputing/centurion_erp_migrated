import pytest

from django.conf import settings
from django.test import Client

from rest_framework.reverse import reverse



class MetadataAttributesFunctionalBase:
    """ Functional Tests for API, HTTP/Options Method
    
    These tests ensure that **ALL** serializers include the metaclass that adds the required
    data to the HTTP Options method.

    Metaclass adds data required for the UI to function correctly.
    """

    app_namespace: str = None

    url_name: str = None

    viewset_type: str = 'list'


    def test_method_options_request_list_ok(self):
        """Test HTTP/Options Method

        Ensure the request returns `OK`.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        assert response.status_code == 200


    def test_method_options_request_list_data_returned(self):
        """Test HTTP/Options Method

        Ensure the request returns data.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        assert response.data is not None


    def test_method_options_request_list_data_type(self):
        """Test HTTP/Options Method

        Ensure the request data returned is of type `dict`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        assert type(response.data) is dict


    def test_method_options_request_detail_ok(self):
        """Test HTTP/Options Method

        Ensure the request returns `OK`.
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

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













    def test_method_options_request_detail_data_has_key_documentation(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `documentation`
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

        assert 'documentation' in response.data


    def test_method_options_request_detail_data_key_documentation_is_str(self):
        """Test HTTP/Options Method

        Ensure the request data key `documentation` is str
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

        assert type(response.data['documentation']) is str


    def test_method_options_request_detail_data_key_documentation_is_url(self):
        """Test HTTP/Options Method

        Ensure the request data key `documentation` is prefixed with settings.DOC_ROOT
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

        assert str(response.data['documentation']).startswith( str(settings.DOCS_ROOT) )









class MetadataAttributesFunctionalTable:
    """Test cases for Metadata
    
    These test cases are for models that are expected to
    be rendered in a table.
    """


    def test_method_options_request_list_data_has_key_table_fields(self):
        """Test HTTP/Options Method

        Ensure the request data returned has key `table_fields`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        assert 'table_fields' in response.data


    def test_method_options_request_list_data_key_table_fields_is_list(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] is of type `list`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        assert type(response.data['table_fields']) is list


    def test_method_options_request_list_data_key_table_fields_is_list_of_str(self):
        """Test HTTP/Options Method

        Ensure the request data['table_fields'] list is of `str`
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type, kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-' + self.viewset_type)

        response = client.options( url, content_type='application/json' )

        all_string = True

        for item in response.data['table_fields']:

            if type(item) is not str:

                all_string = False


        assert all_string



class MetadataAttributesFunctionalEndpoint:
    """Test cases for Metadata
    
    These test cases are for models that will have an
    endpoint. i.e. A Detail view
    """


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



class MetadataAttributesFunctional(
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalTable,
    MetadataAttributesFunctionalBase,
):

    pass



class MetaDataNavigationEntriesFunctional:
    """ Test cases for the Navigation menu

    Navigation menu is rendered as part of the API when a HTTP/OPTIONS
    request has been made. Each menu entry requires that a user has View
    permissions for that entry to be visible.

    **No** menu entry is to be returned for **any** user whom does not 
    have the corresponding view permission.

    These test cases are for any model that has a navigation menu entry.

    ## Tests

    - Ensure add user does not have menu entry
    - Ensure change user does not have menu entry
    - Ensure delete user does not have menu entry
    - Ensure the view user has menu entry
    - No menu to return without pages for add user
    - No menu to return without pages for change user
    - No menu to return without pages for delete user
    - No menu to return without pages for view user
    """

    menu_id: str = None
    """ Name of the Menu entry

    Match for .navigation[i][name]
    """

    menu_entry_id: str = None
    """Name of the menu entry

    Match for .navigation[i][pages][i][name]
    """

    app_namespace:str = None
    """application namespace"""

    url_name: str = None
    """url name"""

    url_kwargs: dict = None
    """View URL kwargs"""

    add_user = None
    """ User with add permission"""

    change_user = None
    """ User with change permission"""

    delete_user = None
    """ User with delete permission"""

    view_user = None
    """ User with view permission"""



    def test_navigation_entry_add_user(self):
        """Test HTTP/Options Method Navigation Entry

        Ensure that a user with add permission, does not
        have the menu entry within navigation
        """

        client = Client()
        client.force_login(self.add_user)


        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options(
            url,
            content_type='application/json'
        )

        assert response.status_code == 403



    def test_navigation_entry_change_user(self):
        """Test HTTP/Options Method Navigation Entry

        Ensure that a user with change permission, does not
        have the menu entry within navigation
        """

        client = Client()
        client.force_login(self.change_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options(
            url,
            content_type='application/json'
        )


        assert response.status_code == 403



    def test_navigation_entry_delete_user(self):
        """Test HTTP/Options Method Navigation Entry

        Ensure that a user with delete permission, does not
        have the menu entry within navigation
        """

        client = Client()
        client.force_login(self.delete_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options(
            url,
            content_type='application/json'
        )


        assert response.status_code == 403



    def test_navigation_entry_view_user(self):
        """Test HTTP/Options Method Navigation Entry

        Ensure that a user with view permission,
        has the menu entry within navigation
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options(
            url,
            content_type='application/json'
        )

        menu_entry_found: bool = False

        for nav_menu in response.data['navigation']:

            if nav_menu['name'] == self.menu_id:

                for menu_entry in nav_menu['pages']:

                    if menu_entry['name'] == self.menu_entry_id:

                        menu_entry_found = True

        assert menu_entry_found



    def test_navigation_no_empty_menu_view_user(self):
        """Test HTTP/Options Method Navigation Entry

        Ensure that a user with view permission, does not
        have any nave menu without pages
        """

        client = Client()
        client.force_login(self.view_user)

        if getattr(self, 'url_kwargs', None):

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        response = client.options(
            url,
            content_type='application/json'
        )

        no_empty_menu_found: bool = True

        for nav_menu in response.data['navigation']:

            if len(nav_menu['pages']) == 0:

                no_empty_menu_found = False

        assert no_empty_menu_found


