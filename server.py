from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.schema import Table, Column, MetaData
from sqlalchemy.ext.automap import automap_base

from config import Config

import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(os.environ['DATABASE_URL'])

Session = sessionmaker(bind=engine)
session = Session()
session.execute("SET search_path to analytical_db_dev, postgis, public")

#Manual approach to declarative object mapping
Base = declarative_base()
Base.metadata = MetaData(bind=engine, schema='analytical_db_dev')
Base.metadata.reflect()

#From here we can construct Table objects to operate on
#g = globals()
#This code doesn't work because not all tables can be automatically mapped
#Those lacking primary keys require extra configuration:
#https://docs.sqlalchemy.org/en/latest/faq/ormconfiguration.html#how-do-i-map-a-table-that-has-no-primary-key

#for tablename, tableobj in Base.metadata.tables.items():
	#g[tablename] = type(str(tablename), (Base,), {'__table__' : tableobj },)
	#g[tablename] = Table(str(tablename), Base.metadata, autoload=True, autoload_with=engine)
#	print("Reflecting {0}".format(tablename))

#Automatically generate classes for every table in the database (warts and all)
#AutomapBase = automap_base()
#AutomapBase.prepare(engine, schema='analytical_db_dev', reflect=True)
#for c in AutomapBase.classes:
#	print("Loaded class: " + str(c))

###flask-sqlalchemy-dependent code here
#db = SQLAlchemy(app)
#db.init_app(app)
#db.app = app
#db.Model.metadata.reflect(bind = db.engine, schema='analytical_db_dev', reflect=True)
#migrate = Migrate(app, db)
###

import routes, models, encoder
app.json_encoder = encoder.CustomJSONEncoder

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
#"An API is a collection of HTTP routes that are designed as 
#low-level entry points into the application"
@app.route("/")
def hello():
	return "Hello World!"