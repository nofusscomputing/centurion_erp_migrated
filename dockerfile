ARG CI_PROJECT_URL=''
ARG CI_COMMIT_SHA=''
ARG CI_COMMIT_TAG=''

ARG ALPINE_VERSION=3.20
ARG NGINX_VERSION=1.27.2-r1
ARG PYTHON_VERSION=3.11.10

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} as build


RUN pip --disable-pip-version-check list --outdated --format=json | \
    python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | \
    xargs -n1 pip install --no-cache-dir -U;


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
        gettext \
        mariadb-client \
        mariadb-dev \
        pkgconf \
        postgresql16-dev \
        postgresql16-client \
        libpq-dev \
        # NginX: to download items
        openssl \
        curl \
        ca-certificates

RUN printf "%s%s%s%s\n" \
  "@nginx " \
  "http://nginx.org/packages/mainline/alpine/v" \
  `egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release` \
  "/main" \
  | tee -a /etc/apk/repositories

RUN curl -o /tmp/nginx_signing.rsa.pub https://nginx.org/keys/nginx_signing.rsa.pub; \
  openssl rsa -pubin -in /tmp/nginx_signing.rsa.pub -text -noout;


  
RUN pip install --upgrade \
    setuptools \
    wheel \
    setuptools-rust \
    twine


COPY requirements.txt /tmp/requirements.txt

COPY requirements_production.txt /tmp/requirements_production.txt


RUN mkdir -p /tmp/python_modules /tmp/python_builds


RUN cd /tmp/python_modules \
  && pip download --dest . --check-build-dependencies \
    -r /tmp/requirements.txt \
    -r /tmp/requirements_production.txt


RUN cd /tmp/python_modules \
  # && export PATH=$PATH:~/.cargo/bin \
  && echo "[DEBUG] PATH=$PATH" \
  && ls -l; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.whl; \
  pip wheel --wheel-dir /tmp/python_builds --find-links . *.tar.gz || true;




FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

LABEL \
  org.opencontainers.image.vendor="No Fuss Computing" \
  org.opencontainers.image.title="Centurion ERP" \
  org.opencontainers.image.description="An ERP with a focus on ITSM and automation" \
  org.opencontainers.image.vendor="No Fuss Computing" \
  io.artifacthub.package.license="MIT"


ARG CI_PROJECT_URL
ARG CI_COMMIT_SHA
ARG CI_COMMIT_TAG

ARG NGINX_VERSION

ENV CI_PROJECT_URL=${CI_PROJECT_URL}
ENV CI_COMMIT_SHA=${CI_COMMIT_SHA}
ENV CI_COMMIT_TAG=${CI_COMMIT_TAG}


COPY requirements.txt requirements.txt
COPY requirements_test.txt requirements_test.txt


COPY ./app/. app

COPY --from=build /tmp/python_builds /tmp/python_builds

COPY --from=build /etc/apk/repositories /etc/apk/repositories

COPY --from=build /tmp/nginx_signing.rsa.pub /etc/apk/keys/nginx_signing.rsa.pub


COPY includes/ /

RUN pip --disable-pip-version-check list --outdated --format=json | \
    python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | \
    xargs -n1 pip install --no-cache-dir -U; \
  apk update --no-cache; \
  apk add --no-cache \
    mariadb-client \
    mariadb-dev \
    postgresql16-client \
    nginx@nginx=${NGINX_VERSION}; \
  pip install --no-cache-dir /tmp/python_builds/*.*; \
    python /app/manage.py collectstatic --noinput; \
    rm -rf /tmp/python_builds; \
    rm /etc/nginx/sites-enabled; \
    ln -s /etc/nginx/sites-available/centurion-erp /etc/nginx/sites-enabled; \
    # Check for errors and fail if so
    nginx -t; \
    # sanity check, https://github.com/nofusscomputing/centurion_erp/pull/370
    if [ ! $(python -m django --version) ]; then \
      echo "Django not Installed"; \
      exit 1; \
    fi; \
    export


WORKDIR /app


EXPOSE 8000

VOLUME [ "/data", "/etc/itsm" ]


HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD \
  supervisorctl status || exit 1


CMD [ "/usr/bin/supervisord" ]
