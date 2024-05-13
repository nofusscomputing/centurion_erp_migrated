FROM python:3.11-alpine3.19 as build


RUN apk add --update \
        bash \
        git \
        gcc \
        cmake \
        libc-dev \
        alpine-sdk \
        libffi-dev \
        build-base \
        curl-dev \
        libxml2-dev \
        gettext

RUN pip install --upgrade \
    setuptools \
    wheel \
    setuptools-rust \
    twine


COPY requirements.txt /tmp/requirements.txt


RUN mkdir -p /tmp/python_modules /tmp/python_builds


RUN cd /tmp/python_modules \
  && pip download --dest . --check-build-dependencies \
    -r /tmp/requirements.txt


RUN cd /tmp/python_modules \
  # && export PATH=$PATH:~/.cargo/bin \
  && echo "[DEBUG] PATH=$PATH" \
  && ls -l; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.whl; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.tar.gz || true;







FROM python:3.11-alpine3.19

COPY requirements.txt requirements.txt
COPY requirements_test.txt requirements_test.txt


COPY ./app/. app

COPY --from=build /tmp/python_builds /tmp/python_builds

RUN pip install /tmp/python_builds/*.*; \
    python /app/manage.py collectstatic --noinput; \
    rm -rf /tmp/python_builds;


WORKDIR /app


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
