---
title: API
description: No Fuss Computings Django Site Template API
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---

to access the api, it can be done with the following command:

``` bash

curl -X GET http://127.0.0.1:8000/api/ -H 'Authorization: Token <token>'

```


## Features

- Inventory Report Collection

- Swagger UI


## Inventory Reports

- url `/api/device/inventory/<device slug>`

- method `POST`

- content `application/json`

Passing a valid inventory report to this endpoint will update the device within the app. If the device doesn't exist it will be created.

Report Format

``` json

{
    "details": {
        "name": "string",
        "serial_number": "string",
        "uuid": "string"
    },
    "os": {
        "name": "name of os",
        "version_major": "major version number",
        "version": "as reported"
    },
    "software": [
        {
            "name": "string",
            "category": "string",
            "version": "string"
        }
    ]
}


```


## User Token

To generate a user token to access the api, use command `python3 manage.py drf_create_token <username>`


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
