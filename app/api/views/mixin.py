
from rest_framework.permissions import DjangoObjectPermissions

from access.mixin import OrganizationMixin



class OrganizationPermissionAPI(DjangoObjectPermissions, OrganizationMixin):
    """checking organization membership"""

    def has_permission(self, request, view):

        return self.permission_check(request, view)


    def has_object_permission(self, request, view, obj):

        return self.permission_check(request, view, obj)


    def permission_check(self, request, view, obj=None) -> bool:

        if request.user.is_anonymous:

            return False

        self.request = request

        if hasattr(view, 'queryset'):
            if view.queryset.model._meta:
                self.obj = view.queryset.model

        method = self.request._request.method.lower()

        object_organization = None

        if method == 'get':

            action = 'view'
        
        elif method == 'post':

            action = 'add'

            if 'organization' in request.data:

                object_organization = int(request.data['organization'])
        
        elif method == 'patch':

            action = 'change'

        elif method == 'put':

            action = 'change'

        elif method == 'delete':

            action = 'delete'

        else:

            action = 'view'

        permission = self.obj._meta.app_label + '.' + action + '_' + self.obj._meta.model_name

        self.permission_required = [ permission ]


        if view:
            if 'organization_id' in view.kwargs:

                if view.kwargs['organization_id']:

                    object_organization = view.kwargs['organization_id']

            if object_organization is None and 'pk' in view.kwargs:

                self.obj = view.queryset.get(pk=view.kwargs['pk'])


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

                    self.obj = view.queryset.get()


        if hasattr(self, 'obj') and object_organization is None and 'pk' in view.kwargs:

            if self.obj.get_organization():

                object_organization = self.obj.get_organization().id

                if hasattr(self.obj, 'is_global'):

                    if self.obj.is_global:

                        object_organization = 0


        # ToDo: implement proper checking of listview as this if allows ALL.
        if 'pk' not in view.kwargs and method == 'get' and object_organization is None:

            return True


        if object_organization is None:

            raise Exception("unable to determine object organization")

        if not self.has_organization_permission(object_organization) and not request.user.is_superuser:
            return False

        return True
