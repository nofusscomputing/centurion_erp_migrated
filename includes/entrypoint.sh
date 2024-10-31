#!/bin/sh

set -e

if [ "$1" == "" ]; then


    echo "[Info] Setup SupervisorD"


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


    echo "[Info] SupervisorD Setup successfully"


    /usr/local/bin/supervisord;


else

    exec "$@"

fi
