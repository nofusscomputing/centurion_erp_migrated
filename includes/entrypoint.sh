#!/bin/sh

set -e

mkdir -p /etc/supervisor/conf.d;

if [ "$1" == "" ]; then


    echo "[Info] Setup SupervisorD"

    if [ ${IS_WORKER} == 'True' ] || [ ${IS_WORKER} == 'true' ]; then


        echo '[info] Creating worker service config';

        cp /etc/supervisor/conf.source/worker.conf /etc/supervisor/conf.d/worker.conf;

        if [ -f '/etc/supervisor/conf.d/worker.conf' ]; then

            echo '[info] Worker service config Created';

        else

            echo '[crit] Worker service config not created';

        fi;


    else

        echo '[info] Creating gunicorn service config';

        cp /etc/supervisor/conf.source/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf;

        if [ -f '/etc/supervisor/conf.d/gunicorn.conf' ]; then

            echo '[info] Gunicorn service config Created';

        else

            echo '[crit] Gunicorn service config not created';

        fi;


        echo '[info] Creating nginx service config';

        cp /etc/supervisor/conf.source/nginx.conf /etc/supervisor/conf.d/nginx.conf;

        if [ -f '/etc/supervisor/conf.d/nginx.conf' ]; then

            echo '[info] NginX service config Created';

        else

            echo '[crit] NginX service config not created';

        fi;


    fi;


    echo "[Info] SupervisorD Setup successfully"


    /usr/local/bin/supervisord;


else

    exec "$@"

fi
