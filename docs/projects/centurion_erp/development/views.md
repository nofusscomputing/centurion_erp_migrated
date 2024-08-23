---
title: Views
description: Centurion ERP Common Views development documentation
date: 2024-07-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

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


## Requirements

All views are to meet the following requirements:

- is defined as a class

- View class inherits from one of the above listed views

- View class has the following attributes definedL

    - `form_class` for the display of [forms](./forms.md).

    - `model` for which data [model](./models.md) to use.

- Add and change views to use a form class


## Tests

The following unit test cases exist for views:

- [AddView](./api/tests/model_views.md#add-view)

- [ChangeView](./api/tests/model_views.md#change-view)

- [DeleteView](./api/tests/model_views.md#delete-view)

- [Display View](./api/tests/model_views.md#display-view)

- [IndexView](./api/tests/model_views.md#index-view)

- [AllViews](./api/tests/model_views.md#all-views)

!!! tip
    The `AllViews` test class is an aggregation of all views. This class is the recommended test class to include if the model uses all available views.


## Docs to clean up

!!! note
    The below documentation is still to be developed. As such what is written below may be incorrect.


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

