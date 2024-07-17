---
title: External Links
description: External Links user documentation for Centurion ERP by No Fuss Computing
date: 2024-07-17
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

External Links allow an end user to specify by means of a jinja template a link that when displayed upon an items display page will add a button with a hyperlink to the url provided. External links can be assigned to: devices and software. This includes both at the same time.


## Create a link

- Software context is under key `software`

- Device context is under key `device`

To add a templated link within the `Link Template` field enter your url, with the variable within jinja braces. for example to add a link that will expand with the devices id, specify `{{ device.id }}`. i.e. `https://domainname.tld/{{ device.id }}`. If the link is for software use key `software`. Available fields under context key all of those that are available at the time the page is rendered.
