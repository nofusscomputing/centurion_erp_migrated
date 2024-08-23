---
title: Installation
description: Installation documentation for Centurion ERP by No Fuss Computing
date: 2024-07-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Centurion ERP is a simple application to deploy with the only additional requirements being that you have already deployed a database server and a RabbitMQ server. Centurion ERP is container based and is deployable via Docker or upon Kubernetes. Our images are available on [Docker Hub](https://hub.docker.com/r/nofusscomputing/centurion-erp).

!!! note "TL;DR"
    `docker pull nofusscomputing/centurion-erp:latest`.


## Installation

Basic installation steps are as follows:

1. Deploy a Database Server

1. Deploy a RabbitMQ Server

1. Deploy a Web container for Centurion ERP

1. Deploy a Worker container for Centurion ERP

1. Add settings file to path `/etc/itsm/settings.py` for both Centurion ERP containers.

1. Run migrations

    - Docker `docker exec -ti <container name or id> -- python manage.py migrate`

    - Kubernetes `kubectl exec -ti -n <namespace> deploy/<deployment-name> -- python manage.py migrate`


### Database Server

As Centurion ERP is uses the Django Framework, Theoretically Every Django supported database is available. The reality is however, that we have only used PostgreSQL Server with Centurion ERP. By default if no database is configured a SQLite database will be used. This allows [tests](../development/testing.md) to function and to quickly spin up a deployment for testing.


### RabbitMQ Server

Centurion ERP uses RabbitMQ as for its worker queue. As tasks are created when using Centurion ERP, they are added to the RabbitMQ server for the background worker to pickup. When the background worker picks up the task, it does it's business, clears the task from the RabbitMQ server and saves the [results](../user/core/index.md#background-worker) within the Database.


### Web Container

The [web container](https://hub.docker.com/r/nofusscomputing/centurion-erp) is the guts of Centurion ERP. It provides the interface and endpoints for interacting with Centurion ERP. This container is scalable with the only additional requirement being that a load-balancer be placed in front of all web containers for traffic routing. If deploying to Kubernetes the service load-balancer is sufficient and setting the deployment `replicas` to the number of desired containers is the simplest method to scale.


### Background Worker Container

The [Background Worker container](https://hub.docker.com/r/nofusscomputing/centurion-erp) is a worker that waits for tasks sent to the RabbitMQ server. The worker is based upon [Celery](https://docs.celeryq.dev/en/stable/index.html). On the worker not being busy, it'll pickup and run the task. This container is scalable with nil additional requirements for launching additional workers. If deploying to Kubernetes the setting the deployment `replicas` to the number of desired containers is the simplest method to scale. The container start command will need to be set to `celery -A app worker -l INFO` so that the worker is started on container startup.

Configuration for the worker resides in directory `/etc/itsm/` within the container. see below for the `CELERY_` configuration.


### Settings file

The settings file is a python file `.py` and must remain a valid python file for the application to work. Settings for the application are stored within a docker volume at path `/etc/itsm/`, with the settings living in `.py` files. A database is also required for the application to store it's settings. SQLLite and MariaDB/MySQL are supported.

``` py title="settings.py"

--8<-- "includes/etc/itsm/settings.py"

```


### Migrations

Migrations serve the purpose of setting up the database. On initial deployment of Centurion ERP migrations must be run as must they be on any upgrade.


## Updating

We use [semver](https://semver.org/) versioning for Centurion ERP. Using this method of versioning enables us to clearly show what versions will have breaking changes. You can rest assured that every version whose `Major` version number remains the same will not break your deployment. [Release notes](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/blob/master/Release-Notes.md) are available within the repository root and are a running document for the current `Major` release. To locate the release notes for your particular version please select the release tag from the branches drop-down. We will use the release notes to denote **Any** Breaking changes.

Updating to a newer version of Centurion ERP is as simple as [backing up your database](./backup.md) and RabbitMQ server, then updating the deployed image to the desired version and running the database migrations.
