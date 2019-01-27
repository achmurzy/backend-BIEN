import json
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import String, Integer
from geoalchemy2 import Geometry

from server import Base

#This class should be used for declaring models when we need to 
#include only a subset of information on the table

class Taxon(Base):
    __table__ = Base.metadata.tables['analytical_db_dev.taxon']

    @property
    def json(self):
        return to_json(self, self.__class__)

class Species(Base):
	__table__ = Base.metadata.tables['analytical_db_dev.species']

	@property
	def json(self):
		return {
            'id': self.id,
            'species': self.species
        }	

class Occurrence(Base):
	__table__ = Base.metadata.tables['analytical_db_dev.view_full_occurrence_individual_dev']

	@property
	def json(self):
		return {
            'longitude': self.longitude,
            'latitude': self.latitude
        }

class Range(Base):
    __tablename__ = 'ranges'
    __table_args__ = {'autoload': True, 'extend_existing': True}
    geom = Column(Geometry('POLYGON'))
    @property
    def json(self):
        return {
            'range': self.geom
        }
    