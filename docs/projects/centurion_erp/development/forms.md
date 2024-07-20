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

- inherits from [`core.forms.common.CommonModelForm`](./api/model_form.md)

- contains a `Meta` sub-class with following parameters:

    - `fields`

    - `model`

- Any additional filtering is done as part of an `__init__` method that also calls the super-class [`__init__`](./api/model_form.md) first

    - Any filtering of a fields `queryset` is to filter the existing `queryset` not redefine it. i.e. `field[<field name>].queryset = field[<field name>].queryset.filter()`

- validating fields where the validation requires access to multiple fields is done inside the form class using function `clean`

    ``` py

    def clean(self):
            
        cleaned_data = super().clean()

        # begin example
        responsible_user = cleaned_data.get("responsible_user")
        responsible_teams = cleaned_data.get("responsible_teams") example


        if not responsible_user and not responsible_teams:

            raise ValidationError('A Responsible User or Team must be assigned.')
        # end example

        # your validation after `super()` call

        return cleaned_data

    ```


## Abstract Classes

The following abstract classes exist for a forms inheritance:

- [AdminGlobalModels](./api/admin_model_form.md#model-form)

- [CommonModelForm](./api/model_form.md#model-form)
