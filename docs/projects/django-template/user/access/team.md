---
title: Team
description: No Fuss Computings Team Documentation for Django ITSM
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

A Team is subordinate to an organization and is a way of grouping permissions with users. A team as the name implies contains application users whom once assigned to a team will be granted the permissions of that team. Permission assigned are an _"allowed"_ to conduct that action. It is not possible to add deny permissions

Team permission are not application wide, their scope is limited to objects that are a part of the same team. In addition any object that is marked `is_global` a user with the objects view permission can see that object.

!!! warning
    An Organization manager can conduct **ALL** operations against a team regardless of their permissions.
