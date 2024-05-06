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

cd itsm

python manage.py runserver 8002

python3 manage.py migrate

python3 manage.py createsuperuser

```

Updates to python modules will need to be captured with SCM. This can be done by running `pip freeze > requirements.txt` from the running virtual environment.
