---
title: Device
description: No Fuss Computings Django Template ITAM Device
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This component within ITAM is intended to display information about a device, be it a computer, router or switch etc.


## Features

For each device within your inventory, the following fields/tabs are available to track items:

- Name

- Operating System

- Software

- Configuration

- Inventory


### Operating System

This tab shows the operating system selected as installed on the device. the version `name` is intended to be full [semver](https://semver.org/).


### Software

This tab displays any action against software. For instance, you can select a piece of software from the inventory and have it set to either `Install` or `Remove` and the ansible config will be updated so that you can pull this config to use within a playbook.

Configuration for this tab is shown as a `list` of `dict` under the configuration key `software` and is setup for ease of use for the `ansible.builtin.apt` module.


### Configuration

Although, configuration is generally part of config management. This tab displays in `JSON` format configuration that is ready for use. The intended audience is Ansible users with the fields provided matching established Ansible modules, if they exist.

This configuration can also be obtained from API endpoint `/api/config/<machine-slug>` where `<machine-slug>` would match the Ansible `inventory_hostname`.


### Inventory

It's possible for a machine to be inventoried and have the report passed to the [inventory endpoint](../api.md#inventory+endpoint). This report will update the device within the interface and provides the option to use scheduled inventory gathering to keep the device up to date.

The report can contain the following information:

- device:

    - `name` Device name

    - `serial number` Device serial number

    - `GUID/UUID` Device GUID/UUID

- operating System

    - `name` Operating system name

    - `version major` Operating system Major version number

    - `installed version` Full [semver](https://semver.org/) of the installed operating system

- software

    - `name` Software Name

    - `category` Software Category

    - `version` Software version

        !!! info
            When the software is added to the inventory, a regex search is done to return the [semver](https://semver.org/) of the software. if no semver is found, the version number provided is used.
