## Version 1.8.0

- Prometheus exporter added. To enable metrics for the database you will have to update the database backend. see the [docs](https://nofusscomputing.com/projects/centurion_erp/administration/monitoring/#django-exporter-setup) for further information.


## Version 1.5.0

- When v1.4.0 was release the migrations were not merged. As part of the work conducted on this release the v1.4 migrations have been squashed. This should not have any effect on any system that when they updated to v1.4, they ran the migrations and they **completed successfully**. Upgrading from <1.4.0 to this release should also have no difficulties as the migrations required still exist. There are less of them, however with more work per migration.

!!! Note
    If you require the previously squashed migrations for what ever reason. Clone the repo and go to commit 17f47040d6737905a1769eee5c45d9d15339fdbf, which is the commit prior to the squashing which is commit ca2da06d2cd393cabb7e172ad47dfb2dd922d952.


## Version 1.4.0

API redesign in preparation for moving the UI out of centurion to it's [own project](https://github.com/nofusscomputing/centurion_erp_ui). This release introduces a **Feature freeze** to the current UI. Only bug fixes will be done for the current UI.
API v2 is a beta release and is subject to change. On completion of the new UI, API v2 will more likely than not be set as stable.

- A large emphasis is being placed upon API stability. This is being achieved by ensuring the following:

    - Actions can only be carried out by users whom have the correct permissions

    - fields are of the correct type and visible when required as part of the API response

    - Data validations work and notify the user of any issue

    We are make the above possible by ensuring a more stringent test policy.

- New API will be at path `api/v2`.

- API v1 is now **Feature frozen** with only bug fixes being completed. It's recommended that you move to and start using API v2 as this has feature parity with API v1.

- API v1 is **depreciated**

- Depreciation of **ALL** API urls. API v1 Will be [removed in v2.0.0](https://github.com/nofusscomputing/centurion_erp/issues/343) release of Centurion.


# Version 1.3.0

!!! danger "Security"
    As is currently the recommended method of deployment, the Centurion Container must be deployed behind a reverse proxy the conducts the SSL termination.

This release updates the docker container to be a production setup for deployment of Centurion. Prior to this version Centurion ERP was using a development setup for the webserver.

- Docker now uses SupervisorD for container

- Gunicorn WSGI setup for Centurion with NginX as the webserver.

- Container now has a health check.

- To setup container as "Worker", set `IS_WORKER='True'` environmental variable within container. _**Note:** You can still use command `celery -A app worker -l INFO`, although **not** recommended as the container health check will not be functioning_


## Version 1.0.0


Initial Release of Centurion ERP.


### Breaking changes

- Nil
