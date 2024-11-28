from rest_framework.relations import Hyperlink



class APICommonFields:
    """Test Cases for fields common to All API responses

    Must contain:
    - id
    - display_name
    - _urls
    - _urls._self
    """


    api_data: object
    """ API Response data """



    def test_api_field_exists_id(self):
        """ Test for existance of API Field

        id field must exist
        """

        assert 'id' in self.api_data


    def test_api_field_type_id(self):
        """ Test for type for API Field

        id field must be int
        """

        assert type(self.api_data['id']) is int


    def test_api_field_exists_display_name(self):
        """ Test for existance of API Field

        display_name field must exist
        """

        assert 'display_name' in self.api_data


    def test_api_field_type_display_name(self):
        """ Test for type for API Field

        display_name field must be str
        """

        assert type(self.api_data['display_name']) is str



    def test_api_field_exists_urls(self):
        """ Test for existance of API Field

        _urls field must exist
        """

        assert '_urls' in self.api_data


    def test_api_field_type_urls(self):
        """ Test for type for API Field

        _urls field must be str
        """

        assert type(self.api_data['_urls']) is dict


    def test_api_field_exists_urls_self(self):
        """ Test for existance of API Field

        _urls._self field must exist
        """

        assert '_self' in self.api_data['_urls']


    def test_api_field_type_urls(self):
        """ Test for type for API Field

        _urls._self field must be str
        """

        assert type(self.api_data['_urls']['_self']) is str



class APIModelFields(
    APICommonFields
):
    """Test Cases for fields common to All API Model responses

    Must contain:
    - id
    - display_name
    - _urls
    - _urls._self
    """


    api_data: object
    """ API Response data """


    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        model_notes field must exist
        """

        assert 'model_notes' in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        model_notes field must be str
        """

        assert type(self.api_data['model_notes']) is str



    def test_api_field_exists_created(self):
        """ Test for existance of API Field

        created field must exist
        """

        assert 'created' in self.api_data


    def test_api_field_type_created(self):
        """ Test for type for API Field

        created field must be str
        """

        assert type(self.api_data['created']) is str



    def test_api_field_exists_modified(self):
        """ Test for existance of API Field

        modified field must exist
        """

        assert 'modified' in self.api_data


    def test_api_field_type_modified(self):
        """ Test for type for API Field

        modified field must be str
        """

        assert type(self.api_data['modified']) is str



class APITenancyObject(
    APIModelFields
):


    api_data: object
    """ API Response data """



    def test_api_field_exists_organization(self):
        """ Test for existance of API Field

        organization field must exist
        """

        assert 'organization' in self.api_data


    def test_api_field_type_organization(self):
        """ Test for type for API Field

        organization field must be dict
        """

        assert type(self.api_data['organization']) is dict



    def test_api_field_exists_organization_id(self):
        """ Test for existance of API Field

        organization.id field must exist
        """

        assert 'id' in self.api_data['organization']


    def test_api_field_type_organization_id(self):
        """ Test for type for API Field

        organization.id field must be dict
        """

        assert type(self.api_data['organization']['id']) is int


    def test_api_field_exists_organization_display_name(self):
        """ Test for existance of API Field

        organization.display_name field must exist
        """

        assert 'display_name' in self.api_data['organization']


    def test_api_field_type_organization_display_name(self):
        """ Test for type for API Field

        organization.display_name field must be str
        """

        assert type(self.api_data['organization']['display_name']) is str


    def test_api_field_exists_organization_url(self):
        """ Test for existance of API Field

        organization.url field must exist
        """

        assert 'url' in self.api_data['organization']


    def test_api_field_type_organization_url(self):
        """ Test for type for API Field

        organization.url field must be str
        """

        assert type(self.api_data['organization']['url']) is Hyperlink
