---
title: Django ITSM
description: No Fuss Computings Django ITSM Application
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

<span style="text-align: center;">

![Project Status - Active](https://img.shields.io/badge/Project%20Status-Active-green?logo=gitlab&style=plastic)

![Gitlab build status - stable](https://img.shields.io/badge/dynamic/json?color=ff782e&label=Stable%20Build&query=0.status&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F57560288%2Fpipelines%3Fref%3Dmaster&logo=gitlab&style=plastic) ![Gitlab build status - development](https://img.shields.io/badge/dynamic/json?color=ff782e&label=Dev%20Build&query=0.status&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F57560288%2Fpipelines%3Fref%3Ddevelopment&logo=gitlab&style=plastic)

![GitLab Issues](https://img.shields.io/gitlab/issues/open/nofusscomputing%2Fprojects%2Fdjango_template?style=plastic&logo=gitlab&label=Issues&color=fc6d26)

![Gitlab Code Coverage](https://img.shields.io/gitlab/pipeline-coverage/nofusscomputing%2Fprojects%2Fdjango_template?branch=master&style=plastic&logo=gitlab&label=Test%20Coverage)

![Docker Pulls](https://img.shields.io/docker/pulls/nofusscomputing/django-template?style=plastic&logo=docker&color=0db7ed)

</span>

This Django Project is designed to be a tool that forms part of IT Service Management (ITSM). The goal is to provide a system that is not only an IT Information Library (ITIL), but that of which will connect to other ITSM systems, i.e. AWX for automation orchestration. Currently the template style is that of the Red Hat echo system (AWX, Foreman, EDA, Cockpit etc).


## Features

This application contains the following module:

- [API](./user/api.md)

- [Application wide settings](./user/settings.md)

- [Configuration Management](./user/config_management/index.md)

- History

- [IT Asset Management (ITAM)](./user/itam/index.md)

- [Multi-Tenant](./user/permissions.md)

Specific features for a module can be found on the module's documentation un the features heading


## Documentation

Documentation is broken down into three areas, they are:

- [Administration](./administration/index.md)

- [Development](./development/index.md)

- [User](./user/index.md)
