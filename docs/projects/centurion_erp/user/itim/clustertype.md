---
title: Cluster Type
description: Cluster Type as part of IT Infrastructure Management Documentation for Centurion ERP by No Fuss Computing
date: 2024-08-18
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This component as part of ITIM is for the classification of a [cluster](./cluster.md), namely the type of cluster.

!!! info
    This feature is ready for further features if desired. i.e. `Cluster Type` configuration. want to see this log a feature request on github.


## Cluster Type

Within the Cluster Type the following fields are available:

- `Name` _name of the cluster type_

- `Organization` _organization the cluster belongs to_

- `Notes` _model notes for cluster type_

- `configuration` _cluster type config_


## Configuration

Configuration can be applied to the cluster type. This configuration is then treated as a template for all clusters of the same type. If the same configuration key is also defined within the cluster, it will take precedence over the cluster type configuration.
