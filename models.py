import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

db = SQLAlchemy()
Base = declarative_base()

class GridCell(Base):
    __tablename__ = "gridcell"
    id = db.Column(db.Integer, primary_key = True)
    #According to geoalchemy2 this creates a spatial index by default, 
    #presumably for Spatialite as well if the extension does what it says it does (Wraps spatialite). Check somehow?
    geom = db.Column(Geometry(geometry_type='POLYGON', management=True)) 
    
class Range(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    geo = db.Column(db.String(64))
    
    @property
    def json(self):
        return {
            'id': self.id,
            'geojson': self.geo
        }

#This might need to happen elsewhere - i.e. only during initialization
#Needed for models derived from Base
#GridCell.__table__.create(db.engine)
#Forecast.__table__.create(db.engine)

#Covers models derived from (db.)Model
#db.create_all()