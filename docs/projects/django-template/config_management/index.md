---
title: Config Management
description: No Fuss Computings Django ITSM Config Management Module
date: 2024-06-03
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

Config Management is an ITSM process that deals with the management and storing of device/host configuration. This module aims to bridge the gap between manual entry of config data via JSON/YAML to entry via a UI. For items that are yet to be integrated into the UI, if at all possible, that config is still manually entered as JSON.  The rendered configuration is intended to be consumed by Ansible. For all intents and purposes, consider this module to be the equivalent of Ansible's host groups.


## Features

This module contains the following features:

- Config Groups

- Assign host to multiple groups

- History


## Config Groups

Considerable thought was placed into as wide a scope as possible, how the host config groups would function. This includes how the end product (the config) would be rendered. To aid in conveying how the config is rendered, consider the following image, which is a basic tree from a single root at the top, with three branches.

![config-merging](../images/config-groups-merging.png)

A host can be assigned to multiple groups as long as the host is not part of the same branch. This image has had each node coloured to denote different groups of the same branch. Note: the red node is a common node for the three branches. for example a host can be placed in each of the three coloured branches. the root node however, if the host is placed in this group then the host can not be placed in any other node. this is because the red node is the root for all three coloured branches.

When it comes time to merge the configuration, if a parent group has the same config as it's childs config. The childs config will take precedence. For a host that is placed in all three branches (orange, green and blue), based of of the group name, sorted alphanumerically, the last group that has conflicting config will be the one that is used. A groups config will always be rendered with it's parents config included all the way up the branch to the root node.
