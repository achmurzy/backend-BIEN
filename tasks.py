from celery import Celery
from celery.contrib.abortable import AbortableTask

import rpy2.rinterface as rinterface
from rpy2.rinterface_lib import openrlib

import numpy as np
import h5py
import random

#Should default to localhost:6379/0, presumably a default in-turn for redis
celery = Celery('tasks', backend='redis://', broker='redis://')

#Could make rinterface from rpy2 a member of these tasks, then each worker gets its own r workspace to run Cory's code in, and retain forecasting results in memory
#Question is whether it will be a nightmare to manage forecasting payloads within R through the layer of rpy2, w.r.t for example memory usage
class SliceTask(AbortableTask):
	def __init__(self):
		self.name = "slice"
		self.forecasts = h5py.File('richness.hdf5', 'r')['data']
	def run(self, grid_cell_indices, year_min, year_max):
		if self.is_aborted():	#For abortion to be effective, this check needs to happen throughout the work
			print("Task aborted during slice")
			return
		local_forecasts = np.take(self.forecasts, grid_cell_indices, 1)
		if self.is_aborted():	#For abortion to be effective, this check needs to happen throughout the work
			print("Task aborted during slice")
			return
		local_forecasts = local_forecasts[slice(year_min, year_max+1, 1), :, :]
		return local_forecasts.tolist()
	def on_failure(self, exc, task_id):
		print("Task caught exception")
		print(exc)
		pass

class RPy2Task(AbortableTask):
	def __init__(self):
		self.name = "rpy2"

	def run(self):	
		rinterface.initr()
		rinterface.baseenv['print'](rinterface.baseenv['getwd']())
		render = rinterface.baseenv['source']('R/render.R')
		grid_cell_indices = rinterface.IntVector([random.randint(0, 100000) for _ in range(100)])
		render[0](grid_cell_indices)
		pass
	
#https://docs.celeryproject.org/en/4.0/whatsnew-4.0.html#the-task-base-class-no-longer-automatically-register-tasks
SliceTask = celery.register_task(SliceTask())
Rpy2Task = celery.register_task(RPy2Task())