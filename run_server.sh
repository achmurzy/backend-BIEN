#!/bin/bash
export FLASK_APP=server.py
export FLASK_ENV=development
gnome-terminal -- celery -A tasks worker --loglevel=INFO
flask run