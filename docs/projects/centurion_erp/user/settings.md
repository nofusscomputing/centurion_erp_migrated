---
title: Settings
description: Settings Module Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-25
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Application settings contain global settings that are applicable to the entire application. Only a super admin can change these settings.


## Global Software

It's possible to enforce that all software is set as global. On defining this setting you must set an organization that the global software will be created in. Then when any software is created it will be set to global and saved to the global organization regardless of the users selected settings.

There is a management command available to manage software globally called `software`. This command enables you to set all software within the application as `global` and to migrate all global software to the global organization, if set. If the application setting `All Software is global` is set as false, any changes to the global status of the software will not move it to the global organization.

- make all software global `python manage.py software -g [--global]`

- Migrate all software to the global organization `python manage.py software -m [--migrate]`


## Global Software Categories

Like global software, a super admin can enforce that all softwre categories be set as global and for it to only be created within the global organization.

There is a management command available to manage software globally called `software_categories`. This command enables you to set all software categories within the application as `global` and to migrate all global software catgeories to the global organization, if set. If the application setting `All Software Categories is global` is set as false, any changes to the global status of the software will not move it to the global organization.

- make all software global `python manage.py software_categories -g [--global]`

- Migrate all software to the global organization `python manage.py software_categories -m [--migrate]`
