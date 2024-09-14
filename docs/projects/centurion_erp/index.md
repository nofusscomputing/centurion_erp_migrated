---
title: Centurion ERP
description: Documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

<span style="text-align: center;">

![Project Status - Active](https://img.shields.io/badge/Project%20Status-Active-green?logo=github&style=plastic)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=master&style=plastic&logo=github&label=Stable%20Build&color=%23000) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/centurion_erp/ci.yaml?branch=development&style=plastic&logo=github&label=Dev%20Build&color=%23000)

![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/nofusscomputing/centurion_erp?style=plastic&logo=github&label=Open%20Issues&color=000) ![GitHub Issues or Pull Requests by label](https://img.shields.io/github/issues/nofusscomputing/centurion_erp/type%3A%3Abug?style=plastic&logo=github&label=Bug%20Fixes%20Required&color=000)

![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_coverage.json&style=plastic) ![Endpoint Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnofusscomputing%2F.github%2Fmaster%2Frepositories%2Fnofusscomputing%2Fcenturion_erp%2Fdevelopment%2Fbadge_endpoint_unit_test.json)


![Docker Pulls](https://img.shields.io/docker/pulls/nofusscomputing/centurion-erp?style=plastic&logo=docker&color=0db7ed) [![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/centurion-erp)](https://artifacthub.io/packages/container/centurion-erp/centurion-erp)

</span>

Whilst there are many Enterprise Rescource Planning (ERP) applications, Centurion ERP is being developed to provide an open source option with a large emphasis on the IT Service Management (ITSM) modules. The goal is to provide a system that is not only an IT Information Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. Other common modules that form part of or are normally found within an ERP system, will be added if they relate specifically to any ITSM workflow. We welcome contributions should you desire a feature that does not yet exist.


## Features

Centurion ERP contains the following modules:

- Change Management

- [Cluster Management](./user/itim/cluster.md)

- [Companion Ansible Collection](../ansible/collections/centurion/index.md)

- [Configuration Management](./user/config_management/index.md)

- **Core Features:**

    - [API](./user/api.md)

    - [Application wide settings](./user/settings/app_settings.md)

    - History

    - [Markdown](./user/core/markdown.md)

    - [Multi-Tenant](./development/api/models/access_organization_permission_checking.md#permission-checking)

    - [Single Sign-On {SSO}](./user/configuration.md#single-sign-on)

- Incident Management

- [IT Asset Management (ITAM)](./user/itam/index.md)

- **Knowledge Management:**

    - [Knowledge Base](./user/assistance/knowledge_base.md)

- Problem Management

- [Project Management](./user/project_management/index.md)

- Request Management

- [Service Management](./user/itim/service.md)


## Documentation

Documentation is broken down into three areas, they are:

- [Administration](./administration/index.md)

- [Development](./development/index.md)

- [User](./user/index.md)

Specific features for a module can be found on the module's documentation un the features heading


## Development

It's important to us that Centurion ERP remaining stable. To assist with this we do test Centurion during it's development cycle. Testing reports are available and can be viewed from [Github](https://github.com/nofusscomputing/centurion_erp/actions/workflows/ci.yaml).

!!! info
    If you find any test that is less than sufficient, or does not exist; please let us know. If you know a better way of doing the test, even better. We welcome your contribution/feedback.


## Roadmap / Planned Features

Below is a list of modules/features we intend to add to Centurion. To find out what we are working on now please view the [Milestones](https://github.com/nofusscomputing/centurion_erp/milestones) on Github.

- **Planned Modules:**

    - Accounting _[see #88](https://github.com/nofusscomputing/centurion_erp/issues/88)_

        General Ledger - _[see #116](https://github.com/nofusscomputing/centurion_erp/issues/116)_

    - Asset Management _[see #89](https://github.com/nofusscomputing/centurion_erp/issues/88)_

    - Core

        - Location Management (Regions, Sites and Locations) _[see #62](https://github.com/nofusscomputing/centurion_erp/issues/62)_

    - Customer Relationship Management (CRM) _[see #91](https://github.com/nofusscomputing/centurion_erp/issues/91)_

    - Database Management _[see #72](https://github.com/nofusscomputing/centurion_erp/issues/72)_

    - Development Operations (DevOPS) _[see #68](https://github.com/nofusscomputing/centurion_erp/issues/58)_

        - Repository Management _[see #115](https://github.com/nofusscomputing/centurion_erp/issues/115)_

    - Human Resource Management _[see #92](https://github.com/nofusscomputing/centurion_erp/issues/92)_

    - IT Asset Management (ITAM)

        - Licence Management _[see #4](https://github.com/nofusscomputing/centurion_erp/issues/4)_

    - IT Infrastructure Management (ITIM) _[see #61](https://github.com/nofusscomputing/centurion_erp/issues/61)_

        - Database Management _[see #72](https://github.com/nofusscomputing/centurion_erp/issues/72)_

        - Software Package Management _[see #96](https://github.com/nofusscomputing/centurion_erp/issues/96)_

        - Role Management _[see #70](https://github.com/nofusscomputing/centurion_erp/issues/70)_

        - Virtual Machine Management _[see #73](https://github.com/nofusscomputing/centurion_erp/issues/73)_

        - Vulnerability Management

            - Software _[see #3](https://github.com/nofusscomputing/centurion_erp/issues/3)_

    - Order Management _[see #94](https://github.com/nofusscomputing/centurion_erp/issues/94)_

        - Supplier Management _[see #123](https://github.com/nofusscomputing/centurion_erp/issues/123)_


- **Planned Integrations:**

    - ArgoCD _[see #77](https://github.com/nofusscomputing/centurion_erp/issues/77)_

        [ArgoCD](https://github.com/argoproj-labs) is a Continuous Deployment system for ensuring objects deployed to kubernetes remain in the desired state.

    - AWX  _[see #113](https://github.com/nofusscomputing/centurion_erp/issues/113)_

        [AWX](https://github.com/ansible/awx) is an Automation Orchestration system that uses Ansible for its configuration.
