#!/bin/bash
export FLASK_APP=server.py
export FLASK_ENV=development
gnome-terminal -- celery -A tasks worker --loglevel=INFO
waitress-serve --call "server:create_app" --host='127.0.0.1' --port='5000'