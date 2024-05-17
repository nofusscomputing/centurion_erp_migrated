---
title: API
description: No Fuss Computings NetBox Django Site Template API
date: 2024-05-15
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---


## Access

to access the api, it can be done with the following command:

``` bash

curl -X GET http://127.0.0.1:8000/api/ -H 'Authorization: Token <token>'

```


## User Token

To generate a user token to access the api, use command `python3 manage.py drf_create_token <username>`
