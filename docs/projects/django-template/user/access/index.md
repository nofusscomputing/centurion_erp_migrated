---
title: Access Module
description: No Fuss Computings Access Module Documentation for Django ITSM
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

The Access module provides the multi-tenancy for this application. Tenancy is organized into organizations, which contain teams which contain users. As part of this module, application permission checking are also conducted. To view the details on how the permissions system works, please view the [application's API documentation](../../development/api/models/access_organization_permission_checking.md).


## Components

- [Organization](./organization.md)

- [Team](./team.md)
