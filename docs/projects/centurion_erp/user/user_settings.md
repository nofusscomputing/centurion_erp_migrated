---
title: User Settings
description: User settings documentation for Centurion ERP by No Fuss Computing
date: 2024-06-29
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

The user settings panel is where all of the logged in users settings reside. Editing of settings is available by clicking on the `Edit` button and adjusting the applicable setting as required.


## Settings

- `Default Organization`

    Default organization for objects to be added to.


## API Tokens

API Tokens are a means by which you can authenticate to the applications [API](api.md) endpoints. To generate a token click on the `Generate Token` button. on the page loading you will be presented with the API token and the opportunity to add a note to the token, generally for reference. You can also adjust the token expiry date, which is the date that the token will expire and no longer work when attempting to access the API when using Token authentication.

!!! danger
    The API token as displayed on the "Token Generation Page" is the only place you are provided the opportunity to obtain the API key. As soon as `Submit` is clicked, the token can no longer be obtained. This is due to the fact that the token is not stored within the application and what is stored can not be reversed into the token itself.
