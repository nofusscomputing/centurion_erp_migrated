---
title: Django ITSM
description: No Fuss Computings Django ITSM
date: 2024-05-06
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This Django Project is designed to be a tool that forms part of IT Service Management (ITSM). The goal is to provide a system that is not only an IT Information Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. Currently the template style is that of the Red Hat echo system (AWX, Foreman, EDA, Cockpit etc).


## Features

This application contains the following module:

- [API](api.md)

- [Application wide settings](settings.md)

- [Configuration Management](config_management/index.md)

- History

- [IT Asset Management (ITAM)](itam/index.md)

- [Multi-Tenant](permissions.md)

Specific features for a module can be found on the module's documentation un the features heading


### History

Effort is placed upon all database items having a history. The items that specifically track history can be found on the items documentation page under its features heading. The history Module tracks the following:

- What Item Type

- What the change was

- Who made the change

- When the change was made

Once a history entry has been made for an item, no one including a `super_admin` can edit or delete a history entry. The only time a history entry is removed, is when an item is removed from the database.

