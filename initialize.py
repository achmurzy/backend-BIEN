from sqlalchemy.sql import select, func
import geojson
import os
import csv
import h5py

from server import db
db.engine.connect().execute(select([func.InitSpatialMetaData(1)]))	#Argument '1' handles the spatial indexing as a single transaction (faster, less safe)

from models import GridCell
GridCell.__table__.create(db.engine)
db.create_all()

def write_forecasts_to_hdf5():
	forecasts = np.stack([np.genfromtxt("../HDR_data/richness_"+str(x)+".csv", delimiter=",") for x in range(2020, 2070)])
	forecast_file = h5py.File('richness', 'w')
	forecast_file.create_dataset('data', data=forecasts)

#Initialize the grid
def load_grid_cells():
	richness = "../HDR_data/richness_present.csv"
	with open(richness) as f:
		forecasts = []	
		csvreader = csv.reader(f)
		next(csvreader, None)	#skip the header
		count = 0
		for row in csvreader: #Given x/y are top-left corners of grid cells in lat/long
			x1 = float(row[0]) #Make geometry by computing bottom-right, 
			y1 = float(row[1])
			x2 = x1 + 0.1		#adding for longitude (-180 -> 180)
			y2 = y1 - 0.08		#subtracting for latitude(90 - > -90)
			x1 = str(x1)
			y1 = str(y1)
			x2 = str(x2)
			y2 = str(y2)
			wkt = "POLYGON(("+x1+" "+y1+","+x2+" "+y1+","+x2+" "+y2+","+x1+" "+y2+"))"
			gc = GridCell(geom=wkt)
			forecasts.append(gc)
			count = count + 1
		db.session.bulk_save_objects(forecasts)
	db.session.commit()