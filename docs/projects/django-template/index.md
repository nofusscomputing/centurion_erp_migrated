---
title: Django Template
description: No Fuss Computings NetBox Django Site Template
date: 2024-04-06
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This Django Project is designed to be a base template for Django applications. It's intent is to contain only the minimal functionality that is/would be common to all Django applications. for instance: base templates, auth and the functions required to make the site navigable. Currently the template style is that of the Red Hat echo system (AWX, Foreman, EDA, Cockpit etc).

This template has built into it multi-tenancy which can easily added to your django application if using this template.


## Features

- [Multi-Tenancy](permissions.md)

- Auto-Generated Navigation Menu


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
