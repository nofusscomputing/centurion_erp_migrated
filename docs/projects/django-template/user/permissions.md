---
title: Permissions
description: No Fuss Computings Django Template Permissions
date: 2024-05-12
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

The base django permissions have not been modified with this app providing Multi-Tenancy. This is done by a mixin, that checks if the item is apart of an organization, if it is; confirmation is made that the user is part of the same organization and as long as they have the correct permission within the organization, access is granted.


## How it works

The overall permissions system of django has not been modified with it remaining fully functional. The multi-tenancy has been setup based off of an organization with teams. A team to the underlying django system is an extension of the django auth group and for every team created a django auth group is created. THe group name is set using the following format: `<organization>_<team name>` and contains underscores `_` instead of spaces.

A User who is added to an team as a "Manager" can modify the team members or if they have permission `access.change_team` which also allows the changing of team permissions. Modification of an organization can be done by the django administrator (super user) or any user with permission `access._change_organization`.

Items can be set as `Global`, meaning that all users who have the correct permission regardless of organization will be able to take action against the object.

Permissions that can be modified for a team have been limited to application permissions only unless adjust the permissions from the django admin site.


## Multi-Tenancy workflow

The workflow is conducted as part of the view and has the following flow:

1. Checks if user is member of organization the object the action is being performed on. Will also return true if the object has field `is_global` set to `true`.

1. Fetches all teams the user is part of.

1. obtains all permissions that are linked to the team.

1. checks if user has the required permission for the action.

1. confirms that the team the permission came from is part of the same organization as the object the action is being conducted on.

1. ONLY on success of the above items, grants access.
