---
title: Forms
description: Centurion ERP Forms development documentation
date: 2024-07-14
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Forms are used within Centurion ERP as the method to display the data from the database. Along with that they are designed to sanitise the user entered data.


## Requirements

All forms must meet the following requirements:

- is defined as a class

- inherits from [`core.forms.common.CommonModelForm`](./api/form.md)

- contains a `Meta` sub-class with following parameters:

    - `fields`

    - `model`

- Any additional filtering is done as part of an `__init__` method that also calls the super-class [`__init__`](./api/form.md) first

    - Any filtering of a fields `queryset` is to filter the existing `queryset` not redefine it. i.e. `field[<field name>].queryset = field[<field name>].queryset.filter()`
