---
title: Monitoring
description: Monitoring documentation for Centurion ERP by No Fuss Computing
date: 2025-01-13
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Monitoring a deployed application is paramount so as to ensure that it is functioning as intended. Without monitoring attempts to fault find an issue become very difficult. Especially when the application has a lot of moving parts. Centurion ERP is no exception.


## Monitoring

To assist in monitoring Centurion ERP, the following features exist:

- Prometheus exporters

- logging _[see #436](https://github.com/nofusscomputing/centurion_erp/issues/436) for more details_


## Prometheus Exporters

Currently we have exporters setup for the following components:

- Django

- Celery Worker, (Django)

- Celery Worker, (Celery)

- NGinX


### Django Exporter Setup

The Django exporter provides metrics on the Django application and a small number of database details. To setup the Django exporter, the following settings are required:

``` py
# Metrics default values
METRICS_ENABLED = False                      # Enable Metrics
METRICS_EXPORT_PORT = 8080                   # Port to serve metrics on
METRICS_MULTIPROC_DIR = '/tmp/prometheus'    # path the metrics from multiple-process' save to

```

Enabling metrics is as simple as adding `METRICS_ENABLED = True` to your Centurion Config File and having prometheus scrape the endpoint. This setting activates the metrics endpoint for both Centurion API and the Centurion Worker. As such, the setting will need to be set in both containers.

!!! danger
    The prometheus endpoint is not secured. As such you are advised against exposing the port publically.

Monitoring of database transactions is possible, however does require that you undate your database backend. for instance, if your using postgres db, the normal backend would be `django.db.backends.postgresql_psycopg2`. This backend does not monitor the database, so it must be modified. this is done by using the prometheus backend `django_prometheus.db.backends.`. So the postgres backend will end up being `django_prometheus.db.backends.postgresql_psycopg2`. The prometheus backend "prefix" is the same for **ALL** backends.
