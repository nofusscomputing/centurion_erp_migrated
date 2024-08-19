---
title: Cluster
description: Cluster as part of IT Infrastructure Management Documentation for Centurion ERP by No Fuss Computing
date: 2024-08-18
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

This component as part of ITIM is for the management of a cluster.


## Features

- Assign Devices as a cluster node

- Assign a Device to be deployed upon a cluster

- Assign configuration for a cluster


## Cluster

Within the services the following fields are available:

- Parent Cluster _Cluster that this cluster is deployed upon_

- [Cluster Type](./clustertype.md) _Type of cluster_

- Name _name of the cluster_

- [Organization](../access/organization.md) _organization this cluster belongs to_

- [Nodes](../itam/device.md) _Cluster Nodes_

- [Devices](../itam/device.md) _Devices deployed upon the cluster_

- [Services](./service.md) _Services deployed upon the cluster_

- Config _Cluster Configuration_

We have designed the cluster management feature to track all that is required to configure, deploy and manage. This allows for a cluster to be deployed to a cluster and to have a cluster span multiple sites and/or locations. i.e. like would be the case having nodes from multiple providers.


### Node

A Cluster Node is a physical or virtual device that the cluster is deployed upon/across. The resources of a node are for the clusters consumption.


### Devices

A Cluster Device is deployed onto the cluster and consumes it resources. This is generally a virtual machine or containerised application.


### Services

A Cluster service is a [service](./service.md) deployed to a cluster. See [#125](https://github.com/nofusscomputing/centurion_erp/issues/125) for it's implementation details.


### Configuration

Cluster configuration is configuration that is used by Ansible to setup/deploy the cluster. The configuration is presented by Centurion ERP within a format that is designed for [our collection](../../../ansible/collections/centurion/index.md).

Configuration if applied within the [cluster type](./clustertype.md#configuration) is used as the base and if also defined within the cluster will take precedence. This allows the cluster type configuration to be used as a base template for clusters of the same type.
