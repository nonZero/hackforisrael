#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source /home/udi/.virtualenvs/h4il/bin/activate
cd $DIR/src
exec gunicorn -p masterpid -b 127.0.0.1:8098 -w 2 h4il.wsgi:application
