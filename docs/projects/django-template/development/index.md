---
title: Django Template Devlopment
description: No Fuss Computings NetBox Django Site Template Development
date: 2024-05-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This page contains different items related to the development of this application.

## Icons

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
