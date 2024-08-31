---
title: Tickets
description: Tickets administration documentation for Centurion ERP by No Fuss Computing
date: 2024-08-27
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The ticketing system within Centurion ERP is common to all ticket types. Available ticket types are as follows:

- Change

- Incident

- Problem

- Request

In addition the following items within Centurion ERP use the ticketing system:

- Git Issue

- Git Merge/Pull Request

- Project Task


## Permissions

Centurion's Tickets have the following permissions:

- add

- change

- comment

- delete

- import

- purge

- triage

- view

Each permission above is constructed into a permission value of `<permission>_ticket_<type>`. For instance an add permission for a request ticket would be constructed as `add_ticket_request`.

Some fields within a ticket are permission based. This means that if a user is missing that permission, they will not be able to change the field in question. The user should not be presented any field they do not have permission to adjust. However if they do manage to change the field, they will be presented with a `HTTP/403` error.

Permissions are exclusive. If a user has not been assigned a permission, they can not perform that action. for instance, if you were to grant a user the "triage" permission, they will not be able to "add" or "view" a ticket. This is by design.

!!! info
    A super-user has permissions to work on any ticket. This also includes any fields.


### Add

The add permissions is designated to allow users to create the ticket. This permission would typically be assigned so that a user could create a ticket A user with this permission can add/edit the following fields:

- `title`

- `description`

- `urgency`


### Change


### Comment

The comment permission is designated to allow users to comment on a ticket. THis permission would typically be assigned to a user so they can comment on a ticket.


### Delete

The add permissions is designated to allow users to delete a ticket. This permission would typically be assigned so that a user could delete a ticket. A user with this permission can add/edit the following fields:

- `is_deleted`

!!! info
    When a ticket is deleted, it still exists within the database. To completely remove a ticket from the database, the `purge` permission is required.


### Import

The import permissions is designated to allow users to import tickets. This permission would typically be assigned so that a user could import tickets from a different ticketing system into Centurion. A user with this permission can add/edit the following fields:

- `external_ref`,
- `external_system`
- `created`
- `date_closed`


### Purge

The purge permissions is designated to allow users to remove tickets from the database to permanently delete them.


### Triage

The triage permissions is designated to allow users to triage tickets. This permission would typically be assigned so that a user can work towards solving the ticket. A user with this permission can add/edit the following fields:

- `impact`
- `priority`
- `project`
- `opened_by`
- `subscribed_users`
- `subscribed_teams`
- `assigned_users`
- `assigned_teams`
- `planned_start_date`
- `planned_finish_date`
- `real_start_date`
- `real_finish_date`


### View

The view permissions is designated to allow users to view **ALL** tickets. This is caveated in the fact that a user will always be able to see their own tickets. The permission would typically be assigned to those whom work with tickets.
