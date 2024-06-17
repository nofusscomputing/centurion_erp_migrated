---
title: Django Template Devlopment
description: No Fuss Computings Django Site Template Development
date: 2024-05-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This page contains different items related to the development of this application.

Documentation for the application api is within it's own section, [API](./api/index.md).


## Icons

To locate additional icons for use see [material icons](https://fonts.google.com/icons).

Icons with text:

- Success `{% include 'icons/success_text.html.j2' with icon_text='success' %}` _denotes yes, success etc_

- Cross `{% include 'icons/cross_text.html.j2' with icon_text='cross' %}` _denotes no, negative etc_

- Change `{% include 'icons/change_text.html.j2' with icon_text='change' %}` _denotes that change management needs to run_

- Issue `{% include 'icons/issue_link.html.j2' with issue=2 %}` _Used to provide a link to an issue on GitLab. i.e. incomplete feature ticket_


## Adding an Application

1. Install the django application with `pip <app-name>`

1. Update `app.settings.py`

    ``` python

    INSTALLED_APPS = [

        '<app name>.apps.<apps.py Class Name>', # Within project directory

        '<app name>',                           # not in project directory

    ]

    ```

1. Update `itsm/urls.py`

    ``` python

    urlpatterns = [

        path("<url path>/", include("<app name>.urls")),

    ]

    ```

!!! tip
    No url from the application will be visible without including the `name` parameter when calling the `path` function within the applications `url.py`. i.e. `urlpatterns[].path(name='<Navigation Name>')`. This is by design and when combined with a prefix of `_` provides the option to limit what URL's are displayed within the navigation menu. A name beginning with an underscore `_` will not be displayed in the menu.

Once you have completed the above list, your application will display collapsed within the navigation menu with the name of your application.


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

from django.db.models import Q

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

        return MyModel.objects.filter(Q(organization__in=self.user_organizations()) | Q(is_global = True))

```

Using a filter `pk__in=self.user_organizations()` for the queryset using the mixins function `user_organizations`, will limit the query set to only items where the user is a member of the organization.


### Templates

The base template includes blocks that are designed to assist in rendering your content. The following blocks are available:

- `title` - The page and title

- `content_header_icon` - Header icon that is middle aligned with the page title, floating right.

- `body` -  The html content of the page

``` html title="template.html.j2"

{% extends 'base.html.j2' %}

{% block title %}{% endblock %}
{% block content_header_icon %}<span title="View History" id="content_header_icon">H</span>{% endblock %}

{% block body %}

your content here

{% endblock %}

```


## Add history to model

The tracking of changes can be added to a model by including the `SaveHistory` mixin from `core.mixin.history_save` to the model.

``` python

from core.mixin.history_save import SaveHistory

class MyModel(SaveHistory):

    .....

```

for items that have a parent item, modification will need to be made to the mixin by adding the relevant check and setting the relevant keys.

``` python

if self._meta.model_name == 'deviceoperatingsystem':

    item_parent_pk = self.device.pk
    item_parent_class = self.device._meta.model_name

```
