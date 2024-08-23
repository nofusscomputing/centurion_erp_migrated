---
title: Core
description: Core Module Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The core module contains items that are relevant across multiple modules.


## Features

- Manufacturers


## Manufacturers

A manufacturer is an entity that creates an item. Within the IT world a manufacturer can also be known as a publisher, this is in the case of software. To add a new manufacturer navigate to `settings -> Common -> Manufacturers / Publishers`


## Background worker

Centurion ERP has a background worker. This worker relies upon RabbitMQ as the broker for storing and routing tasks to workers. Task logs for the jobs ran can be found by navigating to `Settings -> Application -> Task Logs`.
