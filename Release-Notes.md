## Version 1.4.0

- Depreciation of **ALL** API urls. will be [removed in v2.0.0](https://github.com/nofusscomputing/centurion_erp/issues/343) release of Centurion.

- New API will be at path `api/v2` and will remain until v2.0.0 release of Centurion on which the `api/v2` path will be moved to `api`


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
