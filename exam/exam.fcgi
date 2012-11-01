#!/bin/bash

# Replace these three settings.
PROJDIR="/home/statistika/1011/exam"
PIDFILE="$PROJDIR/exam.pid"
SOCKET="$PROJDIR/exam.sock"
HOST="127.0.0.1"
PORT="34001"

cd $PROJDIR
PID=$(cat -- $PIDFILE)
if [ -e /proc/${PID} -a /proc/${PID}/exe -ef python ]; then
    kill $(cat -- $PIDFILE)
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi pidfile=$PIDFILE host=$HOST port=$PORT

