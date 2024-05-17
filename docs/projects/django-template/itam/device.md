---
title: Device
description: No Fuss Computings Django Template ITAM Device
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This component within ITAM is intended to display information about a device, be it a computer, router or switch etc.


## Software

software installed and actions to perform against software


## Configuration

Configuration is rendered in `JSON` format and specifically designed to be compatible with Ansible. This configuration can also be obtained from API endpoint `/api/config/<machine-slug>` where `<machine-slug>` would match the Ansible `inventory_hostname`.
