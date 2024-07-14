---
title: Software
description: Software Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This component within ITAM is intended to display information about software within your inventory. Software can be manually entered into the ITAM database or be added/updated by inventorying a device and uploading a report to the [API endpoint](../api.md#inventory-reports).


## Features

- Details

- Versions

- Installations

- [Change History](../index.md#history)


## Details

This tab displays the details of the software, in particular:

- name

- Publisher

- slug

- category

- organization

- global

!!! info
    If a super admin sets [application setting](../settings.md#global-software) `software is global`, when any software is created, regardless of what organization you set. The software will be created in the "global" organization.


## Versions

This tab displays the different software versions and how many of each version are installed on devices within your inventory.


## Installations

This tab displays the installations of the software on devices within your inventory regardless of version.
