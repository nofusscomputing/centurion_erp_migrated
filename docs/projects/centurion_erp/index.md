---
title: Centurion ERP
description: Documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

<span style="text-align: center;">

![Project Status - Active](https://img.shields.io/badge/Project%20Status-Active-green?logo=gitlab&style=plastic)

![Gitlab build status - stable](https://img.shields.io/badge/dynamic/json?color=ff782e&label=Stable%20Build&query=0.status&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F57560288%2Fpipelines%3Fref%3Dmaster&logo=gitlab&style=plastic) ![Gitlab build status - development](https://img.shields.io/badge/dynamic/json?color=ff782e&label=Dev%20Build&query=0.status&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F57560288%2Fpipelines%3Fref%3Ddevelopment&logo=gitlab&style=plastic)

![GitLab Issues](https://img.shields.io/gitlab/issues/open/nofusscomputing%2Fprojects%2Fcenturion_erp?style=plastic&logo=gitlab&label=Issues&color=fc6d26) [![GitLab Bugs](https://img.shields.io/gitlab/issues/open/nofusscomputing%2Fprojects%2Fcenturion_erp?labels=type%3A%3Abug&style=plastic&logo=gitlab&label=Bug%20Fixes%20Required&color=fc6d26)](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/?sort=created_date&state=opened&label_name%5B%5D=type%3A%3Abug)

![Gitlab Code Coverage](https://img.shields.io/gitlab/pipeline-coverage/nofusscomputing%2Fprojects%2Fcenturion_erp?branch=master&style=plastic&logo=gitlab&label=Test%20Coverage)

![Docker Pulls](https://img.shields.io/docker/pulls/nofusscomputing/centurion-erp?style=plastic&logo=docker&color=0db7ed)

</span>

Whilst there are many Enterprise Rescource Planning (ERP) applications, Centurion ERP is being developed to provide an open source option with a large emphasis on the IT Service Management (ITSM) modules. The goal is to provide a system that is not only an IT Information Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. Other common modules that form part of or are normally found within an ERP system, will be added if they relate specifically to any ITSM workflow. We welcome contributions should you desire a feature that does not yet exist.


## Features

Centurion ERP contains the following modules:

- [Companion Ansible Collection](../ansible/collections/centurion/index.md)

- [Configuration Management](./user/config_management/index.md)

- [IT Asset Management (ITAM)](./user/itam/index.md)


- **Core Features:**

    - [API](./user/api.md)

    - [Application wide settings](./user/settings.md)

    - History

    - [Multi-Tenant](./development/api/models/access_organization_permission_checking.md#permission-checking)

    - [Single Sign-On {SSO}](./user/configuration.md#single-sign-on)


## Documentation

Documentation is broken down into three areas, they are:

- [Administration](./administration/index.md)

- [Development](./development/index.md)

- [User](./user/index.md)

Specific features for a module can be found on the module's documentation un the features heading


## Development

It's important to us that Centurion ERP remaining stable. To assist with this we do test Centurion during it's development cycle. Testing reports are available and can be viewed from [Gitlab](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests) on each Merge Request. You will find a link to the last report conducted as part of that merge request just below the Merge Request's description.

!!! info
    If you find any test that is less than sufficient, or does not exist; please let us know. If you know a better way of doing the test, even better. We welcome your contribution/feedback.


## Roadmap / Planned Features

Below is a list of modules/features we intend to add to Centurion. To find out what we are working on now please view the [Milestones](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/milestones) on Gitlab.

- **Planned Modules:**

    - Accounting _[see #88](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/88)_

        General Ledger - _[see #116](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/116)_

    - Asset Management _[see #89](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/88)_

    - Change Management _[see #90](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/90)_

    - Config Management

        - Host Config _[see #44](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/44)_

    - Core

        - Location Management (Regions, Sites and Locations) _[see #62](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/62)_

    - Customer Relationship Management (CRM) _[see #91](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/91)_

    - Database Management _[see #72](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/72)_

    - Development Operations (DevOPS) _[see #68](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/58)_

        - Repository Management _[see #115](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/115)_

    - Human Resource Management _[see #92](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/92)_

    - Incident Management _[see #93](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/93)_

    - Information Management _[see #10](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/10)_

    - IT Asset Management (ITAM)

        - Licence Management _[see #4](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/4)_

    - IT Infrastructure Management (ITIM) _[see #61](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/61)_

        - Cluster Management _[see #71](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/71)_

        - Database Management _[see #72](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/72)_

        - Service Management _[see #19](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/19)_

        - Software Package Management _[see #96](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/96)_

        - Role Management _[see #70](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/70)_

        - Virtual Machine Management _[see #73](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/73)_

        - Vulnerability Management

            - Software _[see #3](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/3)_

    - Order Management _[see #94](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/94)_

        - Supplier Management _[see #123](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/123)_

    - Project Management _[see #14](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/14)_

    - Problem Management  _[see #95](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/95)_

    - Request Management _[see #96](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/96)_


- **Planned Integrations:**

    - ArgoCD _[see #77](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/77)_

        [ArgoCD](https://github.com/argoproj-labs) is a Continuous Deployment system for ensuring objects deployed to kubernetes remain in the desired state.

    - AWX  _[see #113](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/113)_

        [AWX](https://github.com/ansible/awx) is an Automation Orchestration system that uses Ansible for its configuration.
