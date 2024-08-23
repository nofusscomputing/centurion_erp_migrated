---
title: Backup
description: Backup documentation for Centurion ERP by No Fuss Computing
date: 2024-07-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

Most Data within Centurion ERP resides within the database. This simplifies the backup/restoration process as only the database the application uses needs to be backed up.

Tasks that have been sent to the RabbitMQ server will remain within the task queue, if Centurion ERP has not processed them. Should you wish not to loose tasks you should also backup the rabbitMQ server.
