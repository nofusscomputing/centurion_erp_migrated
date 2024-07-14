# Contribution Guide


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

