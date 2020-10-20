from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from models import db
from redis_config import r as redis

from sqlalchemy.event import listen

def load_spatialite(dbapi_conn, connection_record):
	dbapi_conn.enable_load_extension(True)
	dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

def create_app():
	print("Init flask factory")
	app = Flask(__name__)
	CORS(app)
	app.config.from_object(Config)

	@app.route('/redis_id', methods = ['GET'])
	def assign_client_id():
		user_id = redis.incr('user:id')
		print(user_id)
		return jsonify(user_id)
	db.init_app(app)
	migrate = Migrate(app, db)

	#with app.app_context():
	#	listen(db.engine, 'connect', load_spatialite)
	return app