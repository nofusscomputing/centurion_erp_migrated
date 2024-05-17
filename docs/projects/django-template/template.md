---
title: Template
description: No Fuss Computings Django Template Jinja TEmplate
date: 2024-05-14
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/django_app
---



### Template

The base template includes blocks that are designed to assist in rendering your content. The following blocks are available: 

- `title` - The page and title

- `content_header_icon` - Header icon that is middle aligned with the page title, floating right.

- `body` -  The html content of the page

``` html title="template.html.j2"

{% extends 'base.html.j2' %}

{% block title %}{% endblock %}
{% block content_header_icon %}<span title="View History" id="content_header_icon">H</span>{% endblock %}

{% block body %}

your content here

{% endblock %}

```
