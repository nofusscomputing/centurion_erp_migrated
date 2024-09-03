---
title: Tickets
description: Ticket system Documentation as part of the Core Module for Centurion ERP by No Fuss Computing
date: 2024-08-23
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The ticketing system within Centurion ERP is common to all ticket types. The differences are primarily fields and the value of fields.


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
