import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('user:id', 1000)

def get_slice_task_id_from_redis_with_user_id(user_id):
	key = 'user:'+str(user_id)+':slice'
	task_id = None
	if r.exists(key):
		task_id = r.get(key)
	return task_id

def get_area_of_interest_cells_with_user_id(user_id):
	key = 'user:'+str(user_id)+':cells'
	cells = None
	if r.exists(key):
		cells = json.loads(r.get(key))
	return cells