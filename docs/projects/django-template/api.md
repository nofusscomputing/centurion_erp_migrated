---
title: API
description: No Fuss Computings NetBox Django Site Template API
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
