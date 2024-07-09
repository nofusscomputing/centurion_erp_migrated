---
title: Testing
description: Testing documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Unit tests are written to aid in application stability and to assist in preventing regression bugs. As part of development the developer working on a Merge/Pull request is to ensure that tests are written. Failing to do so will more likely than not ensure that your Merge/Pull request is not merged.

User Interface (UI) test are written to test the user interface to ensure that it functions as it should. Changes to the UI will need to be tested.


## Writing Tests

We use class based tests. Each class will require a `setUpTestData` method for test setup. To furhter assist in the writing of tests, we have written the test cases for common items as an abstract class. You are advised to review the [test cases](./api/tests/index.md) and if it's applicable to the item you have added, than add the test case class to be inherited by your test class.

naming of test classes is in `CamelCase` in format `<Model Name><what's being tested>` for example the class name for device model history entry tests would be `DeviceHistory`.

Test setup is written in a method called `setUpTestData` and is to contain the setup for all tests within the test class.

Test cases themselves are written within the test class within an appropriately and uniquely named method. Each test case is to test **one** and only one item.

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

- CRUD permissions api site - [ModelPermissions (API)](./api/tests/model_permissions_api.md)

- CRUD permissions main site - [ModelPermissions](./api/tests/model_permissions.md)

- can only access organization object - [ModelPermissions](./api/tests/model_permissions.md), [ModelPermissions (API)](./api/tests/model_permissions_api.md)

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


## Running Tests

Test can be run by running the following:

1. `pip install -r requirements_test.txt -r requirements.txt`

1. `pytest --cov --cov-report html --cov=./`

If your developing using VSCode/VSCodium the testing is available as is the ability to attach a debugger to the test.
