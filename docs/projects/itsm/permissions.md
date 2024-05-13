---
title: Un named aPP Permissions
description: No Fuss Computings NetBox ITSM Django APP
date: 2024-05-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

The base django permissions have not been modified with this app adding an addition, which is an organization membership check.


## How it works

No modification has been done to the base Django permissions system. This application provides an additional check for the use in multi-tenancy, which is an membership check for the organization of the object being used.


### Tenancy Setup

Within your view class include the class `OrganizationPermission`, ensuring that you set the `permission_required` attribute.


#### Model Setup

Any item you wish to be multi-tenant, ensure within your model you include the tenancy model abstract class. The class includes a field called `organization` which links directly to an organization and is used by the tenancy permission check.

``` python

from access.models import TenancyObject

from access.models import TenancyObject


class YourObject(TenancyObject):
    ...

```


#### View Setup

``` python

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
