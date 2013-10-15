#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/activate
cd $DIR/src
exec gunicorn -n hackita -p ~/h4il.pid -b 127.0.0.1:8098 -w 2 h4il.wsgi:application
