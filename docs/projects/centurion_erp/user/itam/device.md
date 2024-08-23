---
title: Device
description: Device Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This component within ITAM is intended to display information about a device, be it a computer, router or switch etc.


## Features

For each device within your inventory, the following fields/tabs are available to track items:

- Name

- Model / Manufacturer

- Operating System

- Software

- Configuration

- Inventory

- [Change History](../index.md#history)


### Status at a glance

On the devices list page you can quickly gauge the status of a device. It's a simple colour system: green=OK, red=bad, Orange=Warning and Grey=Unknown. This status icon denotes the age of the last inventory report, being: within 24-hours, within 72-hours, more than 72-hours and unknown. The latter generally indicates that no inventory has been performed.


### Details

This tab display the details of the device.

To add a new model navigate to `settings -> ITAM -> Device Models`

Operating System is also visible on this tab with the version `name` as intended to be full [semver](https://semver.org/).

!!! note
    If you change the devices organization the config groups the device is a part of will be removed.


### Software

- Configuration key `software`

- Format `list of dict`

- Ansible Module `ansible.builtin.apt`

This tab displays both software actions and installed software. Software install details are added/updated by uploading an [inventory report](../api.md#inventory-reports).

You can specify a software action for any piece of software within the ITAM database. You can do this by pressing the `Add Software Action` button or if the software is installed clicking on the `+ Add` button on the row of the software to add the action to. An action can be set to either `Install` or `Remove` and you can also select a software version from the database if you choose to do so. Software actions are added to config management and can be pulled from the API for use within an Ansible playbook.

Display of both installed software and software actions is within a single row, if it's for the same software. Any software that you add an action to, will be displayed at the top of the list of software tab.

!!! info
    If you add a software action for software that is already installed using the `Add Software Action` button, an additional row will not be added as the applications logic is smart enough to check if the software is already installed.


### Configuration

This tab displays in `JSON` format configuration that is ready for use. Config from the [Config Management](../config_management/index.md) module is also included and rendered as part of this config. The intended audience is Ansible users with the fields provided matching established Ansible modules, if they exist.

This configuration can also be obtained from API endpoint `/api/config/<machine-slug>` where `<machine-slug>` would match the Ansible `inventory_hostname`.


### Inventory

!!! tip
    Within your "user settings" you must have a default organization set. Without this the inventory will not be added as this is how the inventory logic determines which organization for the device to be created in.

It's possible for a machine to be inventoried and have the report passed to the [inventory endpoint](../api.md#inventory-reports). This report will update the device within the interface and provides the option to use scheduled inventory gathering to keep the device up to date.

Inventory processing is conducted by a background worker. As soon as the inventory is uploaded, the inventory processing is added to the background worker queue. Further information about the background worker can be found within its [documentation](../core/index.md#background-worker)

!!! tip
    Inventory not uploading? review the task logs by navigating to `Settings -> Application -> Task Logs`

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

Example Report

``` json

{
    "details": {
        "name": "string",
        "serial_number": "string",
        "uuid": "string"
    },
    "os": {
        "name": "name of os",
        "version_major": "major version number",
        "version": "as reported"
    },
    "software": [
        {
            "name": "string",
            "category": "string",
            "version": "string"
        }
    ]
}


```
