from celery import Celery
from celery.contrib.abortable import AbortableTask
import numpy as np
import h5py

#Should default to localhost:6379/0, presumably a default in-turn for redis
celery = Celery('tasks', backend='redis://', broker='redis://')

#Could make rinterface from rpy2 a member of these tasks, then each worker gets its own r workspace to run Cory's code in, and retain forecasting results in memory
#Question is whether it will be a nightmare to manage forecasting payloads within R through the layer of rpy2, w.r.t for example memory usage
class SliceTask(AbortableTask):
	def __init__(self):
		self.name = "slice"
		self.forecasts = h5py.File('richness.hdf5', 'r')['data']
	def run(self, grid_cell_indices, year_min, year_max):
		local_forecasts = np.take(self.forecasts, grid_cell_indices, 1)
		if self.is_aborted():	#For abortion to be effective, this check needs to happen throughout the work
			print("Task aborted")
			return
		local_forecasts = local_forecasts[slice(year_min, year_max+1, 1), :, :]
		return local_forecasts.tolist()
#https://docs.celeryproject.org/en/4.0/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
SliceTask = celery.register_task(SliceTask())