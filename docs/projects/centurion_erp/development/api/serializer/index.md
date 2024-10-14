---
title: Serializers
description: No Fuss Computings Centurion ERP API Documentation for Serializers
date: 2024-06-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This section contains the application API documentation for Serializers to assist in application development. The target audience is anyone whom would be developing the application.

- [Inventory](./inventory.md)


## Requirements

- All Serializers are Class based.

- All models must be serialized.

- Serializer files must contain the following defined serializers:

    - `<Model name>BaseSerializer`

    - `<Model name>ModelSerializer` inheriting `<Model name>BaseSerializer`

    - `<Model name>ViewSerializer` inheriting `<Model name>ModelSerializer`

- Serializers are defined within the `serializer` sub-directory within the app the model is defined.

- Serializer file names are lower case and named the same as the model / related field.

- fields that are required to have an initial value have it specified `self.fields.fields[<field name>].initial`


## Base Serializer

This serializer is read-only and used as the serializer for related items within the model that has this model as related. Must contain the following fields:

- `id` The models primary key

- `display_name` value of model function `__str__()`

- `name` Name/title of the model

- `url` URL to the models page


## Model Serializer

This serializer is write-only and is used for adding and updating a model. This serializer must include all fields the model has. Validation as required is to be done as part of this serializer.


## View Serializer

This serializer is read-only and is used for the viewing of a model within list and detail views. This serializer must define the following fields:

- `_urls` A dictionary of all child models urls

- Each related field redefined as it's base serializer. i.e. `organization = OrganizationBaseSerializer(many=False, read_only=True)`


## Example Serializer

Below is an truncated example serializer.

``` py
from rest_framework.reverse import reverse
from rest_framework import serializers

from itam.models.device import Device



class DeviceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')
    def get_display_name(self, item):

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="API:_api_v2_device-detail", format="html"
    )


    class Meta:

        model = Device

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]


class DeviceModelSerializer(DeviceBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')
    def get_url(self, item):

        return {
            '_self': reverse("API:_api_v2_device-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'software': reverse("API:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
        }


    class Meta:

        model = Device

        fields =  [
             'id',
            'display_name',
            '...',
            'created',
            'modified',
            'organization',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class DeviceViewSerializer(DeviceModelSerializer):

    device_model = DeviceModelBaseSerializer(many=False, read_only=True)
    device_type = DeviceTypeBaseSerializer(many=False, read_only=True)

    organization = OrganizationBaseSerializer(many=False, read_only=True)

```
