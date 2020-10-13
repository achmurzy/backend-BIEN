from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.event import listen

import os

from config import Config

def load_spatialite(dbapi_conn, connection_record):
	dbapi_conn.enable_load_extension(True)
	dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

def create_app():
	app = Flask(__name__)
	CORS(app)
	app.config.from_object(Config)
	return app

app = create_app()

import routes
from models import db

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
	listen(db.engine, 'connect', load_spatialite)

#from waitress import serve 
#serve(app, host='127.0.0.1', port=5000)