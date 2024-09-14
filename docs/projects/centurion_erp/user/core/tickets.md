---
title: Tickets
description: Ticket system Documentation as part of the Core Module for Centurion ERP by No Fuss Computing
date: 2024-08-23
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The ticketing system within Centurion ERP is common to all ticket types. The differences are primarily fields and the value of fields.


## Features

- Commenting

- Related Tickets

- Slash commands

- Ticket Types:

    - Changes

    - Incidents

    - Problems

    - Request

    - Project Task


## Commenting

Comment types are:

- Standard _All Ticket types_

- Notification _Change, Incident, Problem, Project Tasks and Request tickets._

- Solution _Change, Incident, Problem, Project Tasks and Request tickets._

- Task _Change, Incident, Problem, Project Tasks and Request tickets._


## Slash Commands

Slash commands are a quick action that is specified after a slash command. As the name implies, the command starts with a slash `/`. The following slash commands are available:

- Related `/blocked_by`, `/blocks` and `/relate`

- Time Spent `/spend`, `/spent`


### Time Spent

::: app.core.lib.slash_commands.Duration
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


### Related Tickets

::: app.core.lib.slash_commands.CommandRelatedTicket
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


## Ticket Types

::: app.core.models.ticket.ticket.Ticket.TicketType
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true


## Ticket Comments

Within Centurion ERP the ticket comment model is common to all comment types. As with tickets the differences are the available fields, which depend upon comment type and permissions.

::: app.core.models.ticket.ticket_comment.TicketComment.CommentType
    options:
        inherited_members: false
        members: []
        show_bases: false
        show_submodules: false
        summary: true
