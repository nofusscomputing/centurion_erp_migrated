---
title: Configuring
description: Application Configuration documentation for Centurion ERP by No Fuss Computing
date: 2024-06-07
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This page details the configuration for setting up the application.


## Config file

Configuration for this application is stored within a python file `.py` in directory `/etc/istm/`. Any python file placed within this directory will be dynamically loaded at runtime. It's important to ensure that the file remains a valid python file. Failing to do so will prevent the application from restarting.


## Single Sign-On

- `SSO_ENABLED`, boolean

Single Sign on (SSO) is made possible through the [social django application](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html). Specific configuration for the backend that you would like to configure can be viewed within it's [documentation](https://python-social-auth.readthedocs.io/en/latest/backends/index.html). In most cases the only configuration that will need to be defined are for the following attributes: `SSO_ENABLED`, optionally `SSO_BACKENDS` and those with prefix `SOCIAL_AUTH_`.

!!! danger
    Within the social django documentation, it will state the the configuration key for the backends is within attribute `AUTHENTICATION_BACKENDS`, don't use this attribute. Instead use attribute `SSO_BACKENDS` so as not to effect the authentication of the ITSM application.


### Example SSO Configuration

Attributes with prefix `SSO_` are specifically for this application.

``` py

SSO_ENABLED = True             # Optional, boolean. Enable SSO Authentication

SSO_LOGIN_ONLY_BACKEND = 'oidc'    # Optional, string. To only use SSO authentication, specify the backend name here

SSO_BACKENDS = (               # this attribute replaces `AUTHENTICATION_BACKENDS` and must be used instead of.
    "social_core.backends.open_id_connect.OpenIdConnectAuth",
)

# Example configuration for the openid connect backend
SOCIAL_AUTH_OIDC_OIDC_ENDPOINT = 'https://<domain name>/realms/<realm name>'
SOCIAL_AUTH_OIDC_KEY = '<client key>'
SOCIAL_AUTH_OIDC_SECRET = '<client secret>'
# SOCIAL_AUTH_OIDC_SCOPE = ['groups']
# SOCIAL_AUTH_OIDC_IGNORE_DEFAULT_SCOPE = True # default scopes: “openid”, “profile” and “email”

```


## Available Configuration Settings

Below are the available configuration values along with their default value.

``` py

ALLOWED_HOSTS = [ '*' ]          # Site host to serve
DEBUG = False                    # SECURITY WARNING: don't run with debug turned on in production!
SITE_URL = 'http://127.0.0.1'    # domain with HTTP method for the sites URL
SECRET_KEY = None                # You need to generate this
SESSION_COOKIE_AGE = 1209600     # Age the session cookie should live for in seconds. 
SSO_ENABLED = False              # Enable SSO
SSO_LOGIN_ONLY_BACKEND = None    # Use specified SSO backend as the ONLY method to login. (builting login form will not be used)
TRUSTED_ORIGINS = []             # list of trusted domains for CSRF


```
