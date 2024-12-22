from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import ValidationError

from rest_framework import exceptions
from rest_framework.permissions import DjangoObjectPermissions

from access.mixin import OrganizationMixin

from core import exceptions as centurion_exceptions



class OrganizationPermissionAPI(DjangoObjectPermissions, OrganizationMixin):
    """checking organization membership"""

    def has_permission(self, request, view):

        # if view.kwargs.get('pk', None):

        #     if(
        #         str(type(view.get_object()).__name__).lower() == 'organization'
        #     ):

        #         if view.get_object().manager == request.user:

        #             return True

        return self.permission_check(request, view)


    def has_object_permission(self, request, view, obj):

        # if view.kwargs.get('pk', None):

        #     if(
        #         str(type(obj).__name__).lower() == 'organization'
        #     ):

        #         if obj.manager == request.user:

        #             return True

        return self.permission_check(request, view)


    def permission_check(self, request, view, obj=None) -> bool:

        if request.user.is_anonymous:

            return False

        try:

            self.request = request

            method = self.request._request.method.lower()

            if method.upper() not in view.allowed_methods:

                view.http_method_not_allowed(request._request)

            if request.user.is_authenticated and method == 'options':

                return True

            if hasattr(view, 'get_queryset'):

                queryset  = view.get_queryset()

                self.obj = queryset.model

            elif hasattr(view, 'queryset'):

                if view.queryset.model._meta:

                    self.obj = view.queryset.model

            object_organization = None

            if method == 'get':

                action = 'view'
            
            elif method == 'post':

                action = 'add'

                if 'organization' in request.data:

                    print(f'serializer, callable {callable(getattr(view, "get_serializer_class"))},')

                    serializer = None

                    try:    # Method throws exception if not overridden

                        serializer = view.get_serializer_class()

                    except Exception as e:

                        serializer = None

                    try:    # Method throws exception if not overridden

                        serializer = view.get_serializer()

                    except Exception as e:

                        serializer = None


                    if 'organization' not in getattr(serializer.Meta, 'read_only_fields', []):

                        if not request.data['organization']:
                            print('not request.data[organization]')
                            raise centurion_exceptions.ValidationError('you must provide an organization')

                        object_organization = int(request.data['organization'])


            elif method == 'patch':

                action = 'change'

            elif method == 'put':

                action = 'change'

            elif method == 'delete':

                action = 'delete'

            else:

                action = 'view'

            if hasattr(self, 'obj'):
                
                print('permission')

                permission = self.obj._meta.app_label + '.' + action + '_' + self.obj._meta.model_name

                self.permission_required = [ permission ]

            if hasattr(view, 'get_dynamic_permissions'):

                self.permission_required = view.get_dynamic_permissions()


            if view:
                if 'organization_id' in view.kwargs:

                    if view.kwargs['organization_id']:

                        object_organization = view.kwargs['organization_id']

                if object_organization is None and 'pk' in view.kwargs:

                    try:

                        self.obj = view.queryset.get(pk=view.kwargs['pk'])    # Here

                    except ObjectDoesNotExist:

                        return False


                if object_organization is None and getattr(view, 'parent_model', None):

                    parent_model = view.parent_model.objects.get(pk=view.kwargs[view.parent_model_pk_kwarg])

                    object_organization = parent_model.organization.id


            if obj:

                if obj.get_organization():

                    object_organization = obj.get_organization().id

                    if hasattr(self.obj, 'is_global'):
                        
                        if obj.is_global:

                            object_organization = 0


                if 'pk' in view.kwargs:

                    if object_organization is None and view.queryset.model._meta.model_name == 'organization' and view.kwargs['pk']:

                        object_organization = view.kwargs['pk']

                if object_organization is None:

                    try:

                        self.obj = view.queryset.get()

                    except ObjectDoesNotExist:

                        return False


            if hasattr(self, 'obj') and object_organization is None and 'pk' in view.kwargs:

                if self.obj.get_organization():

                    object_organization = self.obj.get_organization().id

                    if hasattr(self.obj, 'is_global'):

                        if self.obj.is_global:

                            object_organization = 0


            # ToDo: implement proper checking of listview as this if allows ALL.
            if 'pk' not in view.kwargs and method == 'get' and object_organization is None:

                return True

            if hasattr(self, 'default_organization'):
                object_organization = self.default_organization

            if method == 'post' and hasattr(self, 'default_organization'):

                if self.default_organization:

                    object_organization = self.default_organization.id

            if not self.has_organization_permission(object_organization) and not request.user.is_superuser:

                raise PermissionDenied('You are not part of this organization')

        except centurion_exceptions.MethodNotAllowed as e:

            raise centurion_exceptions.MethodNotAllowed( str(method).upper() )

        except Exception as e:


            print(f'Exception: {e}')

            return False

        return True
