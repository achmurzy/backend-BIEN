import json
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

from server import db

Base = declarative_base()

class GridCell(Base):
    __tablename__ = "gridcell"
    id = db.Column(db.Integer, primary_key = True)
    #According to geoalchemy2 this creates a spatial index by default, 
    #presumably for Spatialite as well if the extension does what it says it does (Wraps spatialite). Check somehow?
    geom = db.Column(Geometry(geometry_type='POLYGON', management=True)) 
    forecasts = db.relationship("Forecast")
    #Including relationships causes database insertions to slow down and eventually fail. 
    #Either learn how to deal with low-level SQL or master SQLAlchemy

class Forecast(Base):
    __tablename__ = "forecast"
    id = db.Column(db.Integer, primary_key=True)
    grid_cell_id = db.Column(db.Integer, db.ForeignKey(GridCell.id))
    #grid_cell = db.relationship("GridCell", back_populates="forecasts")

    val = db.Column(db.Float)
    year = db.Column(db.Integer)
    #type = db.Column(db.String(64))    #"Diversity" "Drought" "ForestCover" etc

class Range(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    geo = db.Column(db.String(64))
    
    @property
    def json(self):
        return {
            'id': self.id,
            'geojson': self.geo
        }

class RasterCSV(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	csv = db.Column(db.String(64))  

#This might need to happen elsewhere - i.e. only during initialization
#Needed for models derived from Base
#GridCell.__table__.create(db.engine)
#Forecast.__table__.create(db.engine)

#Covers models derived from (db.)Model
#db.create_all()