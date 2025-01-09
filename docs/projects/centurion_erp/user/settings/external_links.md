---
title: External Links
description: External Links user documentation for Centurion ERP by No Fuss Computing
date: 2024-07-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

External Links allow an end user to specify by means of a jinja template a link that when displayed upon an items display page will add a button with a hyperlink to the url provided. External links can be assigned to: devices and software. This includes both at the same time.


## Create a link

- Cluster context is under key `cluster`

- Device context is under key `device`

- Service context is under key `service`

- Software context is under key `software`

To add a templated link within the `Link Template` field enter your url, with the variable within jinja braces. for example to add a link that will expand with the devices id, specify `{{ device.id }}`. i.e. `https://domainname.tld/{{ device.id }}`. If the link is for software use key `software`. Available fields under context key all of those that are available at the time the page is rendered.

!!! tip
    To find out exactly what context is available for a given model, navigate to its API page. The JSON object that is reeturned from the API is the context data. The API path can be derived from the items detail page by suffixing `API/v2` after the domain name, and before the path. i.e. for device one if the url is `https://my-domain.tld/itam/device/1`, its api path is `https://my-domain.tld/api/v2/itam/device/1`


### Filters

Filters enable the ability to perform customizations of the jinja object. Some common filters are:

- `lower` _Convert entire string to lower case letters_

- `upper` _Convert entire string to upper case letters_

For a complete list of available filters please see the [Built-in filters](https://mozilla.github.io/nunjucks/templating.html#builtin-filters) within the documentation.

Filters are simple to use and only require that you enter a pipe `|`, at the end of the jinja object key along with the filter name. For instance, To have a service name converted to lowercase letters, the jinja would be `{{ service.name | lower }}`.
