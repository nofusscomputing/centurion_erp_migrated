---
title: Fields
description: Centurion ERP Fields development documentation
date: 2024-11-13
template: project.html
about: https://github.com/nofusscomputing/centurion_erp
---

Fields are used by the serializers for the data. We have our fields specified in module `core.fields`. These fields are `rest_framework` fields.


## Char Field

This field extends `rest_framework.serializers.CharField` with additional attributes that are used by the UI. The additional attributes are:

- `autolink`, _Boolean_ The interface will render the field as an anchor using the url at path `_urls._self` of the objects data.

- `multiline`, _Boolean_. The field should be rendered as a `textarea` input field.

if attribute `multiline` is not specified, by default the field is rendered as an input text field.


## Markdown Field

This field extends `core.fields.CharField`. The field metadata sets the field type to `Markdown`, which tells the UI to render the field as markdown. The additional attributes are:

- `multiline`, _Boolean_. The field should be rendered as a `textarea` input field.

- `style_class` _String_ This field is a space seperated value (ssv) of CSS classes to use for the field. The UI will use this value as additional CSS classes to append to the field.
