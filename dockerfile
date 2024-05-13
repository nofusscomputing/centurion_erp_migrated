FROM python:3.11-alpine3.19


COPY requirements.txt requirements.txt
COPY requirements_test.txt requirements_test.txt


COPY ./app/. app


RUN pip install --no-cache-dir -r requirements.txt; \
    python /app/manage.py collectstatic --noinput


WORKDIR /app


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
