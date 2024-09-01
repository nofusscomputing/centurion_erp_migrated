---
title: Ticket Object
description: No Fuss Computings Centurion ERP Ticket object API Documentation
date: 2024-09-01
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This page contains the Ticket API Documentation.


## Ticket Status

::: app.core.models.ticket.ticket.Ticket.TicketStatus
    options:
      members: []
      inherited_members: false
      heading_level: 3
      show_submodules: false
      summary: true


## Ticket External System

::: app.core.models.ticket.ticket.Ticket.Ticket_ExternalSystem
    options:
        inherited_members: false
        heading_level: 3


## Ticket Type

::: app.core.models.ticket.ticket.Ticket.TicketType
    options:
        inherited_members: false
        heading_level: 3


## Ticket Urgency

::: app.core.models.ticket.ticket.Ticket.TicketUrgency
    options:
        inherited_members: false
        heading_level: 3


## Ticket Impact

::: app.core.models.ticket.ticket.Ticket.TicketImpact
    options:
        inherited_members: false
        heading_level: 3


## Ticket Priority

::: app.core.models.ticket.ticket.Ticket.TicketPriority
    options:
        inherited_members: false
        heading_level: 3


## Ticket Object Model Abstract class

::: app.core.models.ticket.ticket.Ticket
    options:
        docstring_section_style: table
        inherited_members: false
        heading_level: 3
        filters:
          - "!TicketStatus"
          - "!Ticket_ExternalSystem"
          - "!TicketType"
          - "!TicketUrgency"
          - "!TicketImpact"
          - "!TicketPriority"
