---
title: Models
description: Centurion ERP Models development documentation
date: 2024-07-14
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Models within Centurion ERP are how the data is structured within the database. This page contains documentation pertinent to the development of the models for use with Centurion ERP.


## Requirements

All models must meet the following requirements:

- inherits from `app.access.models.TenancyObject` and `django.db.models.Model`

- class has `__str__` method defined to return that is used to return a default value if no field is specified.

- Fields are initialized with the following parameters:

    - `verbose_name`

    - `help_text`


## Docs to clean up

!!! note
    The below documentation is still to be developed. As such what is written below may be incorrect.


## Model Setup

Any item you wish to be multi-tenant, ensure within your model you include the tenancy model abstract class. The class includes a field called `organization` which links directly to the organization model and is used by the tenancy permission check.

``` python title="<your app name>/models.py"

from access.models import TenancyObject

class YourObject(TenancyObject):
    ...

```


### Add history to model

The tracking of changes can be added to a model by including the `SaveHistory` mixin from `core.mixin.history_save` to the model.

``` python

from core.mixin.history_save import SaveHistory

class MyModel(SaveHistory):

    .....

```

for items that have a parent item, modification will need to be made to the mixin by adding the relevant check and setting the relevant keys.

``` python

if self._meta.model_name == 'deviceoperatingsystem':

    item_parent_pk = self.device.pk
    item_parent_class = self.device._meta.model_name

```
