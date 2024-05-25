---
title: Settings
description: No Fuss Computings Django ITSM Settings
date: 2024-05-25
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

Application settings contain global settings that are applicable to the entire application. Only a super admin can change these settings.


## Global Software

It's possible to enforce that all software is set as global. On defining this setting you must set an organization that the global software will be created in. Then when any software is created it will be set to global and saved to the global organization regardless of the users selected settings.

There is a management command available to manage software globally called `software`. This command enables you to set all software within the application as `global` and to migrate all global software to the global organization, if set. If the application setting `All Software is global` is set as false, any changes to the global status of the software will not move it to the global organization.

- make all software global `python manage.py software -g [--global]`

- Migrate all software to the global organization `python manage.py software -m [--migrate]`
