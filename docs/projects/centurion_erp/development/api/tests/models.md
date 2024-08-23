---
title: Model Test Cases
description: No Fuss Computings model nit test cases
date: 2024-07-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---


## Base Unit Tests for all models

Abstract test class containing test cases for all models.

::: app.app.tests.abstract.models.BaseModel
    options:
        inherited_members: false
        heading_level: 3


## Tenancy model Unit Tests

Abstract test class containing test cases for Tenancy Object models

::: app.app.tests.abstract.models.TenancyModel
    options:
        inherited_members: True
        heading_level: 3
