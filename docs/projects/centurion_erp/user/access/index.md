---
title: Access
description: Access Module Documentation for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The Access module provides the multi-tenancy for this application. Tenancy is organized into organizations, which contain teams which contain users. As part of this module, application permission checking is also conducted.


## Components

- [Organization](./organization.md)

- [Team](./team.md)


## Permission System

The permission system within Centurion ERP is custom and built upon Django's core permission types: add, change, delete and view. For a user to be granted access to perform an action, they must be assigned the permission and have that permission assigned to them as part of the organization they are performing the action in. ALL assigned permissions are limited to the organization the permission is assigned.

!!! tip
    User `A` is in organization `A` and has device view permission. User `A` can view devices in Organization `A` **ONLY**. User `A` although they have the device view permission, can **not** view devices in organization `B`. For User `A` to view devices in organization `B` they would also require the device view permission be assigned to them within organization `B`.

Unlike filesystem based permssions, Centurion ERP permissions are not inclusive, they are mutually exclusive. That is:

- To `add` an item you must have its corresponding `add` permission

- To `change` an item you must have its corresponding `change` permission

- To `delete` an item you must have its corresponding `delete` permission

- To `view` an item you must have its corresponding `view` permission

The exclusitvity is that each of the permissions listed above, dont include an assumed permission. For instance if you have the `add` permission for an item, you will not be able to view it. That would require the `view` permission.
