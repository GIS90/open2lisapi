#!/usr/bin/bash

pwd=$(pwd)
cd $pwd
.venv/bin/gunicorn -c etc/dev/gunicorn.conf wsgi:app