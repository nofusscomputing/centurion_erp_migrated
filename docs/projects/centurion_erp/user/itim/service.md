---
title: Service
description: Service Management Documentation for Centurion ERP by No Fuss Computing
date: 2024-07-21
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This component within ITIM is intended to enable the management of services deployed throughout your IT infrastructure. A service is defined as anything that is deployed that end users would access via a client application. The design of our services is intended to work with either ansible collections or roles. Either way as long as the resulting ansible tasks look for the variables under a single key for the service; any method you choose to deploy a service is up to you.


## Services

Within the services the following fields are available:

- is_template _Defines the service as a template_

- template _name if the template that this service inherits from_

- name _name of the service_

- device _Device service deployed to_

- cluster _Cluster the service is deployed to_

- config _Ansible configuration variables_

- config_key_variable _Ansible dictionary key name for config_

- [port](./port.md) _Ports assosiated with the service_

- dependent_service _A List of services this service depends upon_


## Service Template

A service can be setup as a template `is_template=True` for which then can be used as the base template for further service creations. Both config and Ports are inherited from the template with any conflict taking the current services values.

## Deployed to

A service can be deployed to a Cluster or a Device. When assosiated with an item, within it's details page the services deployed to it are available.
