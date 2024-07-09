---
title: API
description: API Module Documentation for Centurion ERP by No Fuss Computing
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

An api is available for this application and can be viewed at endpoint `/api/`. Documentation specific to each of the endpoints can be found within the swagger UI at endpoint `api/swagger/`.


## Features

- Device Inventory upload

- Swagger UI


## Device Inventory

You can [inventory](itam/device.md#inventory) your devices and upload them to the inventory endpoint.


## Swagger UI

The swagger UI is included within this application and can be found at endpoint `/api/swagger` on your server. This UI has been used to document the API.


## Organizations

- url `/api/organization`, `HTTP/GET` view organizations
- url `/api/organization`, `HTTP/POST` create an organization
- url `/api/organization/<organization id>`, `HTTP/GET` view an organization
- url `/api/organization/<organization id>`, `HTTP/PATCH` edit an organization
- url `/api/organization/<organization id>`, `HTTP/DELETE` delete an organization


## Teams

- url `/api/organization/<organization id>/team`, `HTTP/GET` view teams within org
- url `/api/organization/<organization id>/team`, `HTTP/POST` create team in org
- url `/api/organization/<organization id>/team/<team id>`, `HTTP/GET` view a team in org
- url `/api/organization/<organization id>/team/<team id>`, `HTTP/PATCH` edit team in org
- url `/api/organization/<organization id>/team/<team id>`, `HTTP/DELETE` delete team in org


### Team Permissions

- url `/api/organization/<organization id>/team/<team id>/permissions`, `HTTP/POST` = replace permissions with those in body
- url `/api/organization/<organization id>/team/<team id>/permissions`, `HTTP/PATCH` = amend permissions to include those in body
- url `/api/organization/<organization id>/team/<team id>/permissions`, `HTTP/DELETE` = delete ALL permissions

HTTP/POST or HTTP/PATCH with list of permission in format `<module name>.<permission>_<model>`. i.e for adding a itam device permission would be `itam.add_device`. if the method is post only the permissions in the post request will remain, the others will be deleted. If method is patch, those in request body will be added.
