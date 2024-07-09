---
title: Administration
description: Administration documentation home for Centurion ERP by No Fuss Computing
date: 2024-06-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This documentation is targeted towards those whom administer the applications deployment.


## Installation

To install this application you must have a container engine installed, both docker and kubernetes are supported. The container image is available on [Docker Hub](https://hub.docker.com/r/nofusscomputing/centurion-erp) and can be pulled with `docker pull nofusscomputing/centurion-erp:latest`.

Settings for the application are stored within a docker volume at path `/etc/itsm/`, with the settings living in `.py` files. A database is also required for the application to store it's settings. SQLLite and MariaDB/MySQL are supported.


### Background workers

This application requires that you deploy at least one background worker. The background worker requires access to a RabbitMQ message broker for the queueing and routing of messages (background jobs). If you are using our docker container to deploy this application, launch an additional container with `celery -A app worker -l INFO` as the entrypoint/command. Configuration for the worker resides in directory `/etc/itsm/` within the container. see below for the `CELERY_` configuration.


### Settings file

The settings file is a python file `.py` and must remain a valid python file for the application to work.

``` py title="settings.py"

--8<-- "includes/etc/itsm/settings.py"

```
