from django.utils.safestring import mark_safe

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from access.mixins.organization import OrganizationMixin
from access.mixins.permissions import OrganizationPermissionMixin

from api.auth import TokenScheme
from api.react_ui_metadata import ReactUIMetadata



class Create(
    viewsets.mixins.CreateModelMixin
):


    def create(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().create(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

        return response



class Destroy(
    viewsets.mixins.DestroyModelMixin
):


    def destroy(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().destroy(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

        return response




class List(
    viewsets.mixins.ListModelMixin
):


    def list(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().list(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

        return response


# class PartialUpdate:




class Retrieve(
    viewsets.mixins.RetrieveModelMixin
):


    def retrieve(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().retrieve(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

            else:

                ex = e.get_full_details()

                response = Response(
                    data = {
                        'message': ex['message']
                    },
                    status = e.status_code
                )

        return response



class Update(
    viewsets.mixins.UpdateModelMixin
):


    def partial_update(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().partial_update(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

        return response


    def update(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            response = super().update(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

        return response



class CommonViewSet(
    OrganizationMixin,
    viewsets.ViewSet
):
    """Common ViewSet class

    This class is to be inherited by ALL viewsets.

    Args:
        OrganizationMixin (class): Contains the Authorization checks.
        viewsets (class): Django Rest Framework base class.
    """

    @property
    def allowed_methods(self):
        """Allowed HTTP Methods

        _Optional_, HTTP Methods allowed for the `viewSet`.

        Returns:
            list: Allowed HTTP Methods
        """

        return super().allowed_methods


    documentation: str = None
    """ Viewset Documentation URL

    _Optional_, if specified will be add to list view metadata
    """


    metadata_class = ReactUIMetadata
    """ Metadata Class

    _Mandatory_, required so that the HTTP/Options method is populated with the data
    required to generate the UI.
    """

    model_documentation: str = None
    """Model Documentation URL
    
    _Optional_, if specified will be add to detail view metadata"""

    page_layout: list = []
    """ Page layout class

    _Optional_, used by metadata to add the page layout to the HTTP/Options method
    for detail view, Enables the UI can setup the page layout.
    """

    permission_classes = [ OrganizationPermissionMixin ]
    """Permission Class

    _Mandatory_, Permission check class
    """

    table_fields: list = []
    """ Table layout list

    _Optional_, used by metadata for the table fields and added to the HTTP/Options
    method for detail view, Enables the UI can setup the table.
    """

    view_description: str = None

    view_name: str = None

    def get_back_url(self) -> str:
        """Metadata Back URL

        This URL is an optional URL that if required the view must
        override this method. If the URL for a back operation
        is not the models URL, then this method is used to return
        the URL that will be used.

        Defining this URL will predominatly be for sub-models. It's
        recommended that the `reverse` function
        (rest_framework.reverse.reverse) be used with a `request`
        object.

        Returns:
            str: Full url in format `<protocol>://<doman name>.<tld>/api/<API version>/<model url>`
        """

        return None


    def get_model_documentation(self):

        if not self.model_documentation:

            if hasattr(self.model, 'documentataion'):

                self.model_documentation = self.model.documentation

            else:

                self.model_documentation = ''

        return self.model_documentation


    def get_page_layout(self):

        if len(self.page_layout) < 1:

            if hasattr(self, 'model'):

                if hasattr(self.model, 'page_layout'):

                    self.page_layout = self.model.page_layout

                else:

                    self.page_layout = []

        return self.page_layout


    def get_return_url(self) -> str:
        """Metadata return URL

        This URL is an optional URL that if required the view must
        override this method. If the URL for a cancel operation
        is not the models URL, then this method is used to return
        the URL that will be used.

        Defining this URL will predominatly be for sub-models. It's
        recommended that the `reverse` function
        (rest_framework.reverse.reverse) be used with a `request`
        object.

        Returns:
            str: Full url in format `<protocol>://<doman name>.<tld>/api/<API version>/<model url>`
        """

        return None


    def get_table_fields(self):

        if len(self.table_fields) < 1:

            if hasattr(self, 'model'):

                if hasattr(self.model, 'table_fields'):

                    self.table_fields = self.model.table_fields

                else:

                    self.table_fields = []

        return self.table_fields


    def get_view_description(self, html=False) -> str:

        if not self.view_description:

            self.view_description = ""
        
        if html:

            return mark_safe(f"<p>{self.view_description}</p>")

        else:

            return self.view_description


    def get_view_name(self):

        if getattr(self, 'model', None):

            if self.detail:

                return self.model._meta.verbose_name
            
            return self.model._meta.verbose_name_plural

        if not self.view_name:

            return 'Error'

        return self.view_name




class ModelViewSetBase(
    CommonViewSet
):


    filterset_fields: list = []
    """Fields to use for filtering the query

    _Optional_, if specified, these fields can be used to filter the API response
    """

    model: object = None
    """Django Model
    _Mandatory_, Django model used for this view.
    """

    queryset: object = None
    """View Queryset

    _Optional_, View model Query
    """

    search_fields:list = []
    """ Search Fields

    _Optional_, Used by API text search as the fields to search.
    """


    def get_queryset(self):

        if not self.queryset:

            queryset = self.model.objects.all()

            if 'pk' in self.kwargs:

                if self.kwargs['pk']:

                    queryset = queryset.filter( pk = int( self.kwargs['pk'] ) )

            self.queryset = queryset

        return self.queryset



    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']



class ModelViewSet(
    ModelViewSetBase,
    Retrieve,
    viewsets.ModelViewSet,
):

    pass



class ModelCreateViewSet(
    ModelViewSetBase,
    Create,
    viewsets.GenericViewSet,
):

    pass



class ModelListRetrieveDeleteViewSet(
    ModelViewSetBase,
    List,
    Retrieve,
    Destroy,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to delete and view ONLY!"""

    pass



class ModelRetrieveUpdateViewSet(
    ModelViewSetBase,
    Retrieve,
    Update,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to update and view ONLY!"""

    pass



class ReadOnlyModelViewSet(
    ModelViewSetBase,
    Retrieve,
    List,
    viewsets.GenericViewSet,
):


    pass



class AuthUserReadOnlyModelViewSet(
    ReadOnlyModelViewSet
):
    """Authenticated User Read-Only Viewset

    Use this class if the model only requires that the user be authenticated
    to obtain view permission.

    Args:
        ReadOnlyModelViewSet (class): Read-Only base class
    """

    permission_classes = [
        IsAuthenticated,
    ]


class IndexViewset(
    ModelViewSetBase,
):

    permission_classes = [
        IsAuthenticated,
    ]

