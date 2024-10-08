from flask import jsonify, request, stream_with_context, Response, send_from_directory
from sqlalchemy import and_
from shapely.geometry import asShape
from geoalchemy2.shape import from_shape 
from http import HTTPStatus
import requests, geojson
import numpy as np
from celery.contrib.abortable import AbortableAsyncResult

import subprocess

from server import app
from models import GridCell, db
from tasks import celery, SliceTask, RPy2Task

from redis_config import r as redis
from redis_config import get_slice_task_id_from_redis_with_user_id, get_area_of_interest_cells_with_user_id

@app.route('/rpy2', methods = ['GET'])
def test_rpy2_with_celery():
	RPy2Task().delay()
	return Response()


@app.route('/redis_id', methods = ['GET'])
def assign_client_id():
	user_id = redis.incr('user:id')
	print(user_id)
	return jsonify(user_id)

@app.route("/protected_areas", methods = ['GET'])
def get_protected_areas():
	return Response(redis.get('protected_areas'), mimetype = 'application/json')

@app.route('/forecast', methods = ['POST'])
def forecast():
	user_id = request.json['id']
	task_id = get_slice_task_id_from_redis_with_user_id(user_id)
	if task_id != None:
		result = AbortableAsyncResult(task_id, app=celery)
		print(result.state)
		if result.state != "SUCCESS":
			result.abort()
			#result.revoke() causes errors on the frontend related to abortion
			#result.forget() prevents receipt of results for the final (proper) request
	grid_cell_indices = get_area_of_interest_cells_with_user_id(user_id)
	year_min = request.json['year_min'] - 2020
	year_max = request.json['year_max'] - 2020
	async_result = SliceTask.delay(grid_cell_indices, year_min, year_max)
	redis.set('user:'+str(user_id)+':slice', async_result.id)
	result = ''
	try:	#This raises a ton of errors for tasks that get aborted/revoked
		result = async_result.get() 
	except Exception as e:
		print(e)
	print(len(result))
	return Response(geojson.dumps(result), mimetype = 'application/json')

@app.route('/area_of_interest', methods = ['POST'])
def post_area_of_interest():
	user_id = request.json['id']
	geom = from_shape(asShape(request.json['geojson']['features'][0]['geometry'])) #Right now only supporting one polygon from the featureCollection
	grid_cells = db.session.query(GridCell).filter(GridCell.geom.ST_Intersects(geom)).all()
	grid_cell_indices = [cell.id for cell in grid_cells] 
	redis.set('user:'+str(user_id)+':cells', geojson.dumps(grid_cell_indices))
	return Response(geojson.dumps(grid_cell_indices), mimetype = 'application/json')

def stringify_grid_cells(grid_cells):
	grid_cell_indices = str(grid_cells)
	gg = len(grid_cell_indices)
	grid_cell_indices = grid_cell_indices[1:gg-1]
	return grid_cell_indices

@app.route('/summary', methods = ['GET'])
def send_rmd_summary():
	#p = Process(target=thread_safe_r_compute)
	#p.start()
	#p.join()
	#subprocess.run(["r", "render.R"], input=test_summary_generation(), universal_newlines=True)
	grid_cell_indices = get_area_of_interest_cells_with_user_id(user_id)
	subprocess.run(["r", "render.R"], input=stringify_grid_cells(grid_cell_indices), universal_newlines=True)
	return send_from_directory("summary", "summary.pdf", as_attachment=True) #Need to ensure this is sending the right file i.e. wait until Rmd is finished writing

'''def generate(range_response, range_limit):
	i = 0
	while i < range_limit:
		yield range_response[i].geo
		i = i + 1
	print("Stop iterating")

def generate_protected_areas():
	range_limit = 3
	range_response = db.session.query(Range).limit(range_limit).all()	
	response_generator = generate(range_response, range_limit)
	#Synchronous: get all the ranges and wrap them into one JSON reponse
	#json_response = jsonify([range.geo for range in range_response])
	#return json_response

	#Asynchronous: use a generator to return ranges one at a time
	try:
		protected_area = next(response_generator)
		response = stream_with_context(protected_area)
		return Response(response, mimetype = 'application/json')
	except StopIteration:
		return Response('', mimetype = 'application/json', status = HTTPStatus.NO_CONTENT)'''