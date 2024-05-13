---
title: Permissions
description: No Fuss Computings Django Template Permissions
date: 2024-05-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

The base django permissions have not been modified with this app providing Multi-Tenancy. This is done by a mixin, that checks if the item is apart of an organization, if it is; confirmation is made that the user is part of the same organization and as long as they have the correct permission within the organization, access is granted.


## How it works

The overall permissions system of django has not been modified with it remaining fully functional. The multi-tenancy has been setup based off of an organization with teams. A team to the underlying django system is an extension of the django auth group and for every team created a django auth group is created. THe group name is set using the following format: `<organization>_<team name>` and contains underscores `_` instead of spaces.

A User who is added to an team as a "Manager" can modify the team members or if they have permission `access.change_team` which also allows the changing of team permissions. Modification of an organization can be done by the django administrator (super user) or any user with permission `access._change_organization`.


## Multi-Tenancy workflow

The workflow is conducted as part of the view and has the following flow:

1. Checks if user is member of organization the object the action is being performed on.

1. Fetches all teams the user is part of.

1. obtains all permissions that are linked to the team.

1. checks if user has the required permission for the action.

1. confirms that the team the permission came from is part of the same organization as the object the action is being conducted on.

1. ONLY on success of the above items, grants access.


## Tenancy Setup

Within your view class include the mixin class `OrganizationPermission`, ensuring that you set the `permission_required` attribute.


### Model Setup

Any item you wish to be multi-tenant, ensure within your model you include the tenancy model abstract class. The class includes a field called `organization` which links directly to the organization model and is used by the tenancy permission check.

``` python title="<your app name>/models.py"

from access.models import TenancyObject

class YourObject(TenancyObject):
    ...

```


### View Setup

The mixin inlcuded in this template `OrganizationPermission` is designed to work with all django built in views and is what does the multi-tenancy permission checks.

``` python title="<your app name>/views.py"

from access.mixins import OrganizationPermission

class IndexView(OrganizationPermission, generic.ListView):
    
    model = YourModel

    permission_required = 'access.view_organization'

    # Use this for static success url
    success_url = f"/organization/" + pk_url_kwarg


    # Use this to build dynamic success URL
    def get_success_url(self, **kwargs):

        return f"/organization/{self.kwargs['pk']}/"


    def get_queryset(self):

        return MyModel.objects.filter(organization__in=self.user_organizations())

```

Using a filter `pk__in=self.user_organizations()` for the queryset using the mixins function `user_organizations`, will limit the query set to only items where the user is a member of the organization.
