---
title: Development
description: Development documentation home for Centurion ERP by No Fuss Computing
date: 2024-05-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This section of the documentation contains different items related to the development of this application. The target audience is anyone whom wishes to develop any part of the application.

Centurion ERP is a Django Application. We have added a lot of little tid bits that aid in the development process. i.e. abstract classes, tests etc. This allows for decreased development times as items that are common are what could easily be considered templated with the only additional requirement is to add that objests differences.


## Areas of the code

- [Application API Documentation](./api/index.md)

- [Forms](./forms.md)

- [Models](./models.md)

- [Testing](./testing.md)

- [Views](./views.md)


## Icons

To locate additional icons for use see [material icons](https://fonts.google.com/icons) or [more material icons](https://pictogrammers.com/library/mdi/).

Icons with text:

- Success `{% include 'icons/success_text.html.j2' with icon_text='success' %}` _denotes yes, success etc_

- Cross `{% include 'icons/cross_text.html.j2' with icon_text='cross' %}` _denotes no, negative etc_

- Change `{% include 'icons/change_text.html.j2' with icon_text='change' %}` _denotes that change management needs to run_

- Issue `{% include 'icons/issue_link.html.j2' with issue=2 %}` _Used to provide a link to an issue on GitLab. i.e. incomplete feature ticket_


## Navigation

Within Centurion ERP the navigation menu is dynamically built. To have an item added to the navigation bar to the left of the screen, the following items must be set:

- within the `urlpatterns` list, the path contains the name parameter.

    !!! tip
        Don't use a name that starts with `_`, as this prefix is designed to be used to prevent the url from showing up within the navigation menu

- `app_name = "<app name>"` set in `urls.py`

._Example entry_

``` py title="urls.py"

from django.urls import path

from access.views import organization


app_name = "Access"


urlpatterns = [
    path("", organization.IndexView.as_view(), name="Organizations"),
]

```


## Tenancy Setup

All items within Centurion ERP are considered tenancy objects. Pay particular attention to any requirement that specifies that a class is to be included. Some of these classes add the required logic for Tenancy object CRUD operations as well as permission checking.
