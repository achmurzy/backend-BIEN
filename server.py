from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.event import listen

import os
import geojson

from config import Config
from redis_config import r as redis

def load_spatialite(dbapi_conn, connection_record):
	dbapi_conn.enable_load_extension(True)
	dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

from models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

import routes
with open("protected_areas.json", 'r') as f:
	gj = geojson.dumps(geojson.load(f))
	redis.set('protected_areas', gj)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
	listen(db.engine, 'connect', load_spatialite)

#This won't really work when called directly from python3 
#Instead, we are forced to use waitress-serve then allow this command to take control
from waitress import serve 
serve(app.wsgi_app, host='127.0.0.1', port=5000)