---
title: Django Template
description: No Fuss Computings NetBox Django Site Template
date: 2024-05-06
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This Django Project is designed to be a base template for Django applications. It's intent is to contain only the minimal functionality that is/would be common to all Django applications. for instance: base templates, auth and the functions required to make the site navigable. Currently the template style is that of the Red Hat echo system (AWX, Foreman, EDA, Cockpit etc).

This template has built into it multi-tenancy which can easily added to your django application if using this template.


## Features

- [API](api.md)

- [Multi-Tenancy](permissions.md)

- Auto-Generated Navigation Menu

- [Configuration ready for ansible](itam/device.md#configuration)
