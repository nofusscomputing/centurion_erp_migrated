---
title: Development Documentation
description: No Fuss Computings Development Documentation for Django ITSM
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

This documentation is targeted towards those whom administer the applications deployment.


## Installation

To install this application you must have a container engine installed, both docker and kubernetes are supported. The container image is available on [Docker Hub](https://hub.docker.com/r/nofusscomputing/django-template) and can be pulled with `docker pull nofusscomputing/django-template:latest`.

Settings for the application are stored within a docker volume at path `/etc/itsm/`, with the settings living in `.py` files. A database is also required for the application to store it's settings. SQLLite and MariaDB/MySQL are supported.


### Settings file

The settings file is a python file `.py` and must remain a valid python file for the application to work.

``` py title="settings.py"

--8<-- "includes/etc/itsm/settings.py"

```
