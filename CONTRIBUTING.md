# Contribution Guide


Development of this project has been setup to be done from VSCodium. The following additional requirements need to be met:

- npm has been installed. _required for `markdown` linting_

    `sudo apt install -y --no-install-recommends npm`

- setup of other requirements can be done with `make prepare`

- **ALL** Linting must pass for Merge to be conducted.

    _`make lint`_

## TL;DR


from the root of the project to start a test server use:

``` bash

# activate python venv
/tmp/centurion_erp/bin/activate

# enter app dir
cd app

# Start dev server can be viewed at http://127.0.0.1:8002
python manage.py runserver 8002

# Run any migrations, if required
python manage.py migrate

# Create a super suer if required
python manage.py createsuperuser

```

## Makefile

!!! tip "TL;DR"
    Common make commands are `make prepare` then `make docs` and `make lint`

Included within the root of the repository is a makefile that can be used during development to check/run different items as is required during development. The following make targets are available:

- `prepare`

    _prepare the repository. init's all git submodules and sets up a python virtual env and other make targets_

- `docs`

    _builds the docs and places them within a directory called build, which can be viewed within a web browser_

- `lint`

    _conducts all required linting_

    - `docs-lint`

        _lints the markdown documents within the docs directory for formatting errors that MKDocs may/will have an issue with._

- `clean`

    _cleans up build artifacts and removes the python virtual environment_


> this doc is yet to receive a re-write


# Old working docs


## Dev Environment

It's advised to setup a python virtual env for development. this can be done with the following commands.

``` bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```

To setup the centurion erp test server run the following

``` bash

cd app

python manage.py runserver 8002

python3 manage.py migrate

python3 manage.py createsuperuser

# If model changes
python3 manage.py makemigrations --noinput

# To update code highlight run
pygmentize -S default -f html -a .codehilite > project-static/code.css

```

Updates to python modules will need to be captured with SCM. This can be done by running `pip freeze > requirements.txt` from the running virtual environment.



## Tests

!!! danger "Requirement"
    All models **are** to have tests written for them, Including testing between dependent models. 

See [Documentation](https://nofusscomputing.com/projects/django-template/development/testing/) for further information


## Docker Container

``` bash

cd app

docker build . --tag centurion-erp:dev

docker run -d --rm -v ${PWD}/db.sqlite3:/app/db.sqlite3 -p 8002:8000 --name app centurion-erp:dev

```

