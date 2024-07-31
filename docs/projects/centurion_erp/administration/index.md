---
title: Administration
description: Administration documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This documentation is targeted towards those whom administer the applications deployment.


## Contents

- [Authentication](./authentication.md)

- [Backup](./backup.md)

- [Installation](./installation.md)


## Ansible Automation Platform / AWX

We have built an [Ansible Collection](../../ansible/collections/centurion/index.md) for Centurion ERP that you could consider the bridge between the config within Centurion and the end device. This collection can be directly added to AAP / AWX as a project which enables accessing the features the collection has to offer. Please refer to the [collections documentation](../../ansible/collections/centurion/index.md) for further information.
