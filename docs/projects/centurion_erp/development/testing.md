---
title: Testing
description: Testing documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Unit tests are written to aid in application stability and to assist in preventing regression bugs. As part of development the developer working on a Merge/Pull request is to ensure that tests are written. Failing to do so will more likely than not ensure that your Merge/Pull request is not merged.

User Interface (UI) test are written _if applicable_ to test the user interface to ensure that it functions as it should. Changes to the UI will need to be tested.

!!! note
    As of release v1.3, the UI has moved to it's [own project](https://github.com/nofusscomputing/centurion_erp_ui) with the current Django UI feature locked and depreciated.

In most cases functional tests will not need to be written, however you should confirm this with a maintainer.

Integration tests **will** be required if the development introduces code that interacts with an independent third-party application.


## Available Test classes

To aid in development we have written test classes that you can inherit from for your test classes

- API Permission Checks

    _These test cases ensure that only a user with the correct permissions can perform an action against a Model within Centurion_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionAdd` _Add permission checks_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionChange` _Change permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionDelete` _Delete permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissionView` _View permission check_

    - `api.tests.abstract.api_permissions_viewset.APIPermissions` _Add, Change, Delete and View permission checks_

- API Field Checks

    _These test cases ensure that all of the specified fields are rendered as part of an API response_

    - `api.tests.abstract.api_fields.APICommonFields` _Fields that should be part of ALL API responses_

    - `api.tests.abstract.api_fields.APIModelFields` _Fields that should be part of ALL model API Responses. Includes `APICommonFields` test cases_

    - `api.tests.abstract.api_fields.APITenancyObject` _Fields that should be part of ALL Tenancy Object model API Responses. Includes `APICommonFields` and `APIModelFields` test cases_


## Writing Tests

We use class based tests. Each class will require a `setUpTestData` method for test setup. To furhter assist in the writing of tests, we have written the test cases for common items as an abstract class. You are advised to inherit from our test classes _(see above)_ as a starting point and extend from there.

Naming of test classes is in `CamelCase` in format `<Model Name><what's being tested>` for example the class name for device model history entry tests would be `DeviceHistory`.

Test setup is written in a method called `setUpTestData` and is to contain the setup for all tests within the test class.

Test cases themselves are written within the test class within an appropriately and uniquely named method. Each test case is to test **one** and only one item.

Example of a model history test class.

``` py

import pytest
import requests

from django.test import TestCase, Client

from core.models.history import History
from core.tests.abstract.history_entry import HistoryEntry
from core.tests.abstract.history_entry_parent_model import HistoryEntryParentItem



class DeviceHistory(TestCase, HistoryEntry, HistoryEntryParentItem):


    model = Device


    @classmethod
    def setUpTestData(self):
        """ Setup Test """

```

Each module is to contain a tests directory of the model being tested with a single file for grouping of what is being tested. for items that depend upon a parent model, the test file is to be within the child-models test directory named with format `test_<model>_<parent app>_<parent model name>`

example file system structure showing the layout of the tests directory for a module.

``` text
.
├── tests
│   ├── functional
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   ├── __init__.py
│   ├── integration
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── <model name>
│   │       └── test_<model name>_a_tast_name.py
│   └── unit
│       ├── __init__.py
│       └── <model name>
│           ├── test_<model name>_api.py
│           ├── test_<model name>_permission_api.py
│           ├── test_<model name>_permission.py
│           ├── test_<model name>_core_history.py
│           ├── test_<model name>_history_permission.py
│           ├── test_<model name>.py
│           └── test_<model name>_viewsets.py

```

Tests are broken up into the type the test is (sub-directory to test), and they are `unit`, `functional`, `UI` and `integration`. These sub-directories each contain a sub-directory for each model they are testing.

Items to test include, and are not limited to:

- CRUD permissions admin site

- CRUD permissions api site

- can only access organization object

- can access global object (still to require model CRUD permission)

- history - [History Entries](./api/tests/model_history.md), [History Permissions](./api/tests/model_history_permissions.md)

    - saves history with parent pk and parent class

        add to model class the following

        ``` py

        @property
        def parent_object(self):
            """ Fetch the parent object """
            
            return self.<item that is the parent>

        ```

        history should now be auto saved as long as class `core.mixin.history_save.SaveHistory` is inherited by model.

    - history is deleted when item deleted if `parent_pk=None` or if has `parent_pk` deletes history on parent pk being deleted.

- model - _any customizations_

- notes - [Notes Permissions](./api/tests/notes_permissions.md)

    _applicable if notes are able to be added to an item._

- API Fields

    _Field(s) exists, Type is checked_


## Running Tests

Test can be run by running the following:

1. `pip install -r requirements_test.txt -r requirements.txt`

1. `pytest --cov --cov-report html --cov=./`

If your developing using VSCode/VSCodium the testing is available as is the ability to attach a debugger to the test.
