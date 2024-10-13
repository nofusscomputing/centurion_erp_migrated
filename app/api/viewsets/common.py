from django.utils.safestring import mark_safe

from rest_framework import viewsets

from access.mixin import OrganizationMixin

from api.react_ui_metadata import ReactUIMetadata
from api.views.mixin import OrganizationPermissionAPI



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

    permission_classes = [ OrganizationPermissionAPI ]
    """Permission Class

    _Mandatory_, Permission check class
    """

    view_description: str = None

    view_name: str = None


    def get_view_description(self, html=False) -> str:

        if not self.view_description:

            self.view_description = ""
        
        if html:

            return mark_safe(f"<p>{self.view_description}</p>")

        else:

            return self.view_description


    def get_view_name(self):

        if hasattr(self, 'model'):

            if self.detail:

                return self.model._meta.verbose_name
            
            return self.model._meta.verbose_name_plural

        if not self.view_name:

            return 'Error'

        return self.view_name




class ModelViewSet(
    viewsets.ModelViewSet,
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

    model_documentation: str = None
    """Model Documentation URL
    
    _Optional_, if specified will be add to detail view metadata"""

    page_layout: list = []
    """ Page layout class

    _Optional_, used by metadata to add the page layout to the HTTP/Options method
    for detail view, Enables the UI can setup the page layout.
    """

    queryset: object = None
    """View Queryset

    _Optional_, View model Query
    """

    search_fields:list = []
    """ Search Fields

    _Optional_, Used by API text search as the fields to search.
    """


    def get_model_documentation(self):

        if not self.model_documentation:

            if hasattr(self.model, 'documentataion'):

                self.model_documentation = self.model.documentation

            else:

                self.model_documentation = ''

        return self.model_documentation


    def get_page_layout(self):

        if len(self.page_layout) < 1:

            if hasattr(self.model, 'page_layout'):

                self.page_layout = self.model.page_layout

            else:

               self.page_layout = []

        return self.page_layout


    def get_queryset(self):

        if not self.queryset:

            self.queryset = self.model.objects.all()
        
        return self.queryset



    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']