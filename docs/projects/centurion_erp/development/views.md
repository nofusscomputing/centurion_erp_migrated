---
title: Views
description: Views development Documentation for Centurion ERP
date: 2024-07-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Views are used with Centurion ERP to Fetch the data for rendering.

!!! info
    Centurion release v1.3.0 added a feature lock to **ALL** Views and the current API. From this release, there is a new API at endpoint `api/v2`. As such we will only be using DRF `ViewSets`. This is required as the UI is being separated from the Centurion Codebase to its own repository. This means that Centurion will become an API only codebase. Release 2.0.0 will remove the current UI and api from Centurion. [See #](https://github.com/nofusscomputing/centurion_erp/issues/343) for details.


## Requirements

- Views are class based

- Inherits from one of the following base class':

    - Index Viewset `api.viewsets.common.CommonViewSet`

    - Model Viewset `api.viewsets.common.ModelViewSet`

    - Model Viewset that are to be Read-Only `api.viewsets.common.ReadOnlyModelViewSet`

- **ALL** views are `ViewSets`

- Views are saved within the module the model is from under path `viewsets/`

- views are documented at the class level for the swagger UI.

- Index Viewsets must be tested against tests `from api.tests.abstract.viewsets import ViewSetCommon`

- Model VieSets must be tested against the following tests:

    - _Unit Test Cases_ `from api.tests.abstract.viewsets import ViewSetModel`

    - _Functional test cases_ `from api.tests.abstract.api_serializer_viewset import SerializersTestCases`

    - _Functional test cases_ `from api.tests.abstract.api_permissions_viewset import APIPermission`

- View Added to Navigation


## Permissions

If you wish to deviate from the standard CRUD permissions, define a function called `get_dynamic_permissions` within the `view`/`ViewSet`. The function must return a list of permissions. This is useful if you have added additional permissions to a model.

Example of the function `get_dynamic_permissions`

``` py

def get_dynamic_permissions(self):

    if self.action == 'create':

        self.permission_required = [
            'core.random_permission_name',
        ]

    else:

        raise ValueError('unable to determine the action_keyword')

    return super().get_permission_required()

```


## Navigation

Although Centurion ERP is a Rest API application, there is a UI. The UI uses data from Centurion's API to render the view that the end user sees. One of those items is the navigation structure.

Location of the navigation is in `app/api/react_ui_metadata.py` under the attribute `_nav`.


### Menu Entry

When adding a view, that is also meant to be seen by the end user, a navigation entry must be added to the correct navgation menu. The entry is a python dictionary and has the following format.

``` pyhton

{
    '<app name>.<permission name>': {
        "display_name": "<menu entry name>",
        "name": "<html id>",
        "icon": "<menu entry icon>",
        "link": "<relative url.>"
    }
}

```

- `app name` _Optional_ is the centurion application name the model belongs to. This entry should only be supplied if the application name for the entry does not match the application for the [navigation menu](#menu).

- `permission name` is the centurion permission required for this menu entry to be rendered for the end user.

- `display_name` Menu entry name that the end user will see

- `name` This is used as part of the html rendering of the page. **must be unique** across ALL menu entries

- `icon` _Optional_ if specified, this is the name of the icon that the UI will place next to the menu entry. If this is not specified, the name key is used as the icon name.

- `link` the relative URL for the entry. this will be the relative URL of the API after the API's version number. _i.e. `/api/v2/assistance/ticket/request` would become `/assistance/ticket/request`_


### Menu

The navigation menu is obtained by the UI as part of the metadata. The structure of the menu is a python dictionary in the following format:

``` python

 {
        '<app name>': {
            "display_name": "<Menu entry>",
            "name": "<menu id>",
            "pages": {
                '<menu entries>'
            }
        }
 }

```

- `app name` the centurion application name the menu belongs to.

- `display_name` Menu name that the end user will see

- `name` This is used as part of the html rendering of the page. **must be unique** across ALL menu entries

- `pages` [Menu entry](#menu-entry) dictionaries.

Upon the UI requesting the navigation menu, the users permission are obtained, and if they have the permission for the menu entry within **any** organization, they will be presented with the menu that has a menu entries.


## Pre v1.3 Docs

!!! warning
    These docs are depreciated

Views are used with Centurion ERP to Fetch the data for rendering as html. We have templated our views to aid in quick development. We have done this by adding to our views the required pieces of logic so as to ensure the right information is available. The available API can be found within the [API Views](./api/common_views.md) docs.

The views that we use are:

- [Index](./api/common_views.md#index-view)

    Models index page

- [Add](./api/common_views.md#add-view)

    For adding data to model tables

- [Change](./api/common_views.md#change-view)

    Changing data within a model

- [Delete](./api/common_views.md#delete-view)

    Delete a model

- [Display](./api/common_views.md#display-view)

    Display a model

Common test cases are available for views. These test cases can be found within the API docs under [model view test cases](./api/tests/model_views.md).


### Requirements - Depreciated

All views are to meet the following requirements:

- is defined as a class

- View class inherits from one of the above listed views

- View class has the following attributes definedL

    - `form_class` for the display of [forms](./forms.md).

    - `model` for which data [model](./models.md) to use.

- Add and change views to use a form class


### Tests

The following unit test cases exist for views:

- [AddView](./api/tests/model_views.md#add-view)

- [ChangeView](./api/tests/model_views.md#change-view)

- [DeleteView](./api/tests/model_views.md#delete-view)

- [Display View](./api/tests/model_views.md#display-view)

- [IndexView](./api/tests/model_views.md#index-view)

- [AllViews](./api/tests/model_views.md#all-views)

!!! tip
    The `AllViews` test class is an aggregation of all views. This class is the recommended test class to include if the model uses all available views.


### Docs to clean up

!!! note
    The below documentation is still to be developed. As such what is written below may be incorrect.


#### Templates

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
