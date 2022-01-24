#!/bin/bash

# usage: pm2 start ./run.sh
source venv/bin/activate
gunicorn -w 2 -k gevent --log-level=info --worker-connections 1000 -b 0.0.0.0:8021 app:app
