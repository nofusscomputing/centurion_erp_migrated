---
title: Project
description: No Fuss Computings Project User Documentation for Django ITSM
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

Projects enable the grouping and management of tasks within a single location/item.


## Fields

- Reference Number

    _External Reference Number imported from. **Import user only.**_

- External System

    _External System imported from. **Import user only.**_

- Description

    _Description of the project. [Markdown](../core/markdown.md) is supported._

- Priority

    _Priority of the project_

- State

    _[State](./project_state.md) of the project_

- Type

    _[Project Type](./project_type.md)_

- Completed

    _This field automagically calculates the percentage of the project tasks completed_

- Duration

    _This field automagically calculates the time spent on the project. This is derived from the time spent on tasks assigned to to the project._

- Code

    _Reference code for the project_

- Planned Start Date

    _When the project is scheduled to start_

- Planned Finish Date

    _When the project is scheduled to finish_

- Real Start Date

    _When the project actually started_

- Real Finish Date

    _When the project actually finished_

- Manager User

    _Who is the assigned project manager user_

- Manager Team

    _which team is aassigned as the project manager_

- Team Members

    _Users who are the Project Team Members_


## Milestones

Projects can have milestones created. These milestones can then be assigned to [project tasks](./project_task.md).

## Tasks

A Project can have tasks added to it. be it a [project task](./project_task.md) or any other ticket type available. To assign a ticket to a project, when editing the ticket select the desired project.
