# Contribution Guide


## Dev Environment

It's advised to setup a python virtual env for development. this can be done with the following commands.

``` bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```

To setup the django test server run the following

``` bash

cd app

python manage.py runserver 8002

python3 manage.py migrate

python3 manage.py createsuperuser

# If model changes
python3 manage.py makemigrations --noinput

```

Updates to python modules will need to be captured with SCM. This can be done by running `pip freeze > requirements.txt` from the running virtual environment.



## Tests

!!! danger "Requirement"
    All models **are** to have tests written for them, Including testing between dependent models. 

To ensure consistency and reliability of this application, tests are to be written. Each test is to test one item ONLY and no more. Each module is to contain a tests directory of the model being tested with a single file for grouping of what is being tested. for items that depend upon a parent model, the test file is to be within the child-models test directory named with format `test_<model>_<parent app>_<parent model name>`

_example structure for the device model that relies upon access app model organization, core app model history and model notes._

``` text

├── tests
│   ├── <model name>
│   │   ├── test_<model name>_access_organization.py
│   │   ├── test_<model name>_api_permission.py
│   │   ├── test_<model name>_core_history.py
│   │   ├── test_<model name>_core_notes.py
│   │   ├── test_<model name>_permission.py
│   │   └── test_device.py


```

Items to test include but are not limited to:

- CRUD permissions admin site

- CRUD permissions api site

- CRUD permissions main site

- can only access organization object

- can access global object (still to require model CRUD permission)

- model

- history

    - saves history with parent pk and parent class

        add to model class the following
        ``` py
        @property
        def parent_object(self):
            """ Fetch the parent object """
            
            return self.<item that is the parent>
        ```

        history should now be auto saved as long as class `core.mixin.history_save.SaveHistory` is inherited by model.

    - history is deleted when item deleted if `parent_pk=None` or if has `parent_pk` deletes history on parent pk being deleted.


### Running Tests

test can be run by running the following:

1. `pip install -r requirements_test.txt -r requirements.txt`

1. `pytest --cov --cov-report html --cov=./`


## Docker Container

``` bash

cd app

docker build . --tag django-app:dev

docker run -d --rm -v ${PWD}/db.sqlite3:/app/db.sqlite3 -p 8002:8000 --name app django-app:dev

```

