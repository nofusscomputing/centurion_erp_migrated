---
title: Unit Tests
description: No Fuss Computings django itsm unit tests
date: 2024-06-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

Unit tests are written to aid in application stability and to assist in preventing regression bugs. As part of development the developer working on a Merge/Pull request is to ensure that tests are written. Failing to do so will more likely than not ensure that your Merge/Pull request is not merged.


## Writing Tests

We use class based tests. Each class will require a `setUpTestData` method for test setup. To furhter assist in the writing of tests, we have written the test cases for common items as an abstract class. You are advised to review the [test cases](#test-cases) and if it's applicable to the item you have added, than add the test case class to be inherited by your test class.

naming of test classes is in `CamelCase` in format `<Model Name><what's being tested>` for example the class name for device model history entry tests would be `DeviceHistory`.

Test setup is written in a method called `setUpTestData` and is to contain the setup for all tests within the test class.

Example of a model history test class.

``` py

import pytest
import unittest
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

_example file system structure for the device model that relies upon access app model organization, core app model history and model notes._

``` text

├── tests
│   ├── <model name>
│   │   ├── test_<model name>_access_organization.py
│   │   ├── test_<model name>_api_permission.py
│   │   ├── test_<model name>_core_history.py
│   │   ├── test_<model name>_core_notes.py
│   │   ├── test_<model name>_permission.py
│   │   └── test_device.py


```

Items to test include, and are not limited to:

- CRUD permissions admin site

- CRUD permissions api site

- CRUD permissions main site

- can only access organization object

- can access global object (still to require model CRUD permission)

- model

- history

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


## Running Tests

Test can be run by running the following:

1. `pip install -r requirements_test.txt -r requirements.txt`

1. `pytest --cov --cov-report html --cov=./`

If your developing using VSCode/VSCodium the testing is available as is the ability to attach a debugger to the test.


## Test Cases

Models are tested using the following test cases:

- [ALL Model Permission](./model_permissions.md)

- [Add Permission](./model_permission_add.md)

- [Change Permission](./model_permission_change.md)

- [Delete Permission](./model_permission_delete.md)

- [View Permission](./model_permission_view.md)

- [ALL API Model Permission](./model_permissions_api.md)

- [API Add Permission](./model_permission_api_add.md)

- [API Change Permission](./model_permission_api_change.md)

- [API Delete Permission](./model_permission_api_delete.md)

- [API View Permission](./model_permission_api_view.md)

- [History Entry](./model_history.md)

- [History Entry (Child Item)](./model_history_child_item.md)

- [History Entry (Parent Item)](./model_history_parent_item.md)

- [History Entry Permissions](./model_history_permissions.md)
