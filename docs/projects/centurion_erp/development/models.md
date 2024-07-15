---
title: Models
description: Centurion ERP Models development documentation
date: 2024-07-14
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Models within Centurion ERP are how the data is structured within the database. This page contains documentation pertinent to the development of the models for use with Centurion ERP.

All models within Centurion ERP are what we call a "Tenancy Object." A tenancy object is a model that takes advantage of the multi-tenancy features of Centurion ERP.


## Requirements

All models must meet the following requirements:

- inherits from [`app.access.models.TenancyObject`](./api/models/tenancy_object.md)

    !!! tip
        There is no requirement to include class [`app.core.mixin.history_save.SaveHistory`](./api/models/core_history_save.md) for inheritence as this class is already included within class [`app.access.models.TenancyObject`](./api/models/tenancy_object.md).

    !!! note
        If there is a specific use case for the object not to be a tenancy object, this will need to be discussed with a maintainer.

- class has `__str__` method defined to return that is used to return a default value if no field is specified.

- Fields are initialized with the following parameters:

    - `verbose_name`

    - `help_text`

- No `queryset` is to return data that the user has not got access to. _see [queryset()](./api/models/tenancy_object.md#tenancy-object-manager)_


## Docs to clean up

!!! note
    The below documentation is still to be developed. As such what is written below may be incorrect.

for items that have a parent item, modification will need to be made to the mixin by adding the relevant check and setting the relevant keys.

``` python

if self._meta.model_name == 'deviceoperatingsystem':

    item_parent_pk = self.device.pk
    item_parent_class = self.device._meta.model_name

```
