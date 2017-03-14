import json
import os
import numpy
from datetime import datetime, timedelta
from body_sensor import body_sensor
import glob
import pytz
import math
import matplotlib.pyplot as plt

class DataRun():
	def __init__(self):
		self.data = {}
		self.time_info = {}
		self.start_time = pytz.UTC.localize(datetime.now())
		self.end_time = pytz.UTC.localize(datetime.now())
		self.title = ""
	
	def update_start_end(self, name):
		if self.time_info[name] == []:
			print("No info found for string \"{}\"".format(name))
		if max(self.time_info[name]) > self.end_time:
			self.end_time = max(self.time_info[name])
		if min(self.time_info[name]) < self.start_time:
			self.start_time = min(self.time_info[name])

	def load_data(self, file_name="*.json"):
		for name in glob.glob(file_name):
			type = ""
			with open(name, 'r') as data_file:
				type = json.load(data_file)[0]['$type'].split(".")[-1].split(",")[0]
			if type == "MicrosoftBandAccelerometerDatum":
				data_array, time_stamp_array = body_sensor.get_accel_data(name)
				self.data['accelerometer'] = data_array
				self.time_info['accelerometer'] = time_stamp_array
				self.update_start_end('accelerometer')
			elif type == "MicrosoftBandHeartRateDatum":
				data_array, time_stamp_array = body_sensor.get_heart_rate_data(name)
				self.data['heartrate'] = data_array
				self.time_info['heartrate'] = time_stamp_array
				self.update_start_end('heartrate')
			elif type == "MicrosoftBandGyroscopeDatum":
				data_array, time_stamp_array = body_sensor.get_gyroscope_data(name)
				self.data['gyroscope'] = data_array
				self.time_info['gyroscope'] = time_stamp_array
				self.update_start_end('gyroscope')
			elif type == "MicrosoftBandGsrDatum":
				data_array, time_stamp_array = body_sensor.get_gsr_data(name)
				self.data['gsr'] = data_array
				self.time_info['gsr'] = time_stamp_array
				self.update_start_end('gsr')
			elif type == "MicrosoftBandSkinTemperatureDatum":
				data_array, time_stamp_array = body_sensor.get_skin_temp_data(name)
				self.data['skin_temp'] = data_array
				self.time_info['skin_temp'] = time_stamp_array
				self.update_start_end('skin_temp')
			#more added later

	def show_data(self, data_type, index_by_time=False, datasets=-1, one_graph=False):
		data = self.data[data_type]
		index_count = 10
		plt.figure(1)
		range_size = 0
		if datasets == -1:
			range_size = data.shape[0]
		else:
			if datasets >= data.shape[0]:
				range_size = data.shape[0]
			else:
				range_size = datasets
		for i in range(0, range_size):
			if not one_graph:
				plt.subplot(range_size, 1, i+1)
			if index_by_time:
				rel_time = []
				start = self.time_info[data_type][0]
				for c_time in self.time_info[data_type]:
					delt = c_time-start
					rel_time.append(delt.seconds)
				plt.plot(sorted(rel_time), data[i, :])
			else:
				plt.plot(data[i, :])
		plt.show()
	
	def show_fft(self, data_type, datasets=-1, filter_fft=True, treshold=0.05):
		data = self.data[data_type]
		plt.figure(1)
		range_size = 0
		if datasets == -1:
			range_size = data.shape[0]
		else:
			if datasets >= data.shape[0]:
				range_size = data.shape[0]
			else:
				range_size = datasets
		for i in range(0, range_size):
			data[i, :] -= data[i, :].mean()
			transform = numpy.fft.fft(data[i, :])
			if filter_fft:
				transform = numpy.convolve(transform, [1/5, 1/5, 1/5, 1/5, 1/5])
			plt.subplot(range_size, 1, i+1)
			plt.plot(transform)
			plt.axis([-10, len(transform)*0.27, transform.min()*1.1, transform.max()*1.1])
		plt.show()

	def display_data_run(self, data_types=[], one_graph=False, index_by_time=True, time_range=(0, 0), show_plot=True):
		fig = plt.figure()
		if data_types == []: #empty list indicates all data types to be displayed
			data_types = list(self.data.keys())
		if one_graph == False:
			for plot in range(0, len(data_types)):
				data_type = data_types[plot]
				if data_type not in list(self.data.keys()):
					continue
				ax = plt.subplot(len(data_types), 1, plot+1)
				data = self.data[data_type]
				time = self.time_info[data_type]
				ax.set_ylabel(data_type)
				for i in range(0, data.shape[0]):
					if index_by_time:
						rel_time = []
						start = time[0]
						for c_time in time:
							delt = c_time-start
							if not time_range == (0, 0):
								if delt.seconds < time_range[0]:
									continue
								if  delt.seconds > time_range[1]:
									break
							rel_time.append(float(delt.seconds) + float(delt.microseconds/1000000))
						plt.plot(rel_time, data[i, :len(rel_time)])
					else:
						plt.plot(data[i, :])
		else: #for plotting all graphs on same axes - can't figure out how to do different scales
			pass
		if show_plot:
			plt.show()
		else:
			return fig

	def find_fourier_edge(self, fourier, width=65, thresh=0.05):
		for i in range(0, len(fourier)):
			if (i + width) >= len(fourier):
				break
			if fourier[i:i+width].max() <= fourier.max()*0.05:
				return i + width
	
	def make_figure_with_fourier(self, raw_data, label):
		#fig = plt.figure(label)
		#plt.subplot(211)
		data = raw_data - raw_data.mean()
		data = numpy.convolve(data, [1/100, 1/95, 1/88, 1/80, 1/70, 1/55, 1/38, 1/24, 1/10, 1/2, 1/10, 1/24, 1/38, 1/55, 1/70, 1/80, 1/88, 1/95, 1/100])
		#plt.plot(data)
		#plt.title(label)
		fourier = numpy.fft.fft(data)
		#plt.subplot(212)
		plt.plot(fourier)
		plt.axis([-10, self.find_fourier_edge(fourier), fourier.max()*1.2, fourier.min()*1.2])
		#return fig

	def save_data_figures(self, run, label_text):
		data = self.data[run]
		label_mat = ['X', 'Y', 'Z']
		plt.clf()
		plt.figure(1)
		for i in range(0, data.shape[0]):
			plt.subplot(3, 1, i+1)
			self.make_figure_with_fourier(data[i, :], label_text)
			#plt.figure(fig.number)
		plt.savefig("{} - {}.png".format(label_text, run))
