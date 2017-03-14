import os
import json
import numpy
from datetime import datetime

def get_time(time_string):
	format_string = "%Y-%m-%dT%H:%M:%S.%f%z"
	date_time = time_string[:-3] + time_string[-2:]
	return datetime.strptime(date_time, format_string)

def sort_by_time(time_array, data_array):
	time_index_array = numpy.argsort(time_array)
	sorted_time_array = list()
	sorted_data_array = numpy.zeros_like(data_array)
	for index, item in enumerate(time_index_array):
		if sorted_data_array.shape[0] == 1:
			sorted_data_array[0, index] = data_array[0, item]
		else:
			sorted_data_array[:, index] = data_array[:, item]
		sorted_time_array.append(time_array[item])
	return sorted_data_array, sorted_time_array

def get_accel_data(json_file_name):
	data_in = []
	with open(json_file_name, 'r') as data_file:
		data_in = json.load(data_file)
	data_array = numpy.zeros((3, len(data_in)))
	time_stamp_array = []
	for index, point in enumerate(data_in):
		time_stamp_array.append(get_time(point['Timestamp']))
		data_array[0, index] = point['X']
		data_array[1, index] = point['Y']
		data_array[2, index] = point['Z']
	return sort_by_time(time_stamp_array, data_array)

def get_heart_rate_data(json_file_name):
	data_in = []
	with open(json_file_name, 'r') as data_file:
		data_in = json.load(data_file)
	data_array = numpy.zeros((1, len(data_in)))
	time_stamp_array = []
	for index, point in enumerate(data_in):
		time_stamp_array.append(get_time(point['Timestamp']))
		data_array[0, index] = point['HeartRate']
	return sort_by_time(time_stamp_array, data_array)

def get_gyroscope_data(json_file_name):
	data_in = []
	with open(json_file_name, 'r') as data_file:
		data_in = json.load(data_file)
	data_array = numpy.zeros((3, len(data_in)))
	time_stamp_array = []
	for index, point in enumerate(data_in):
		time_stamp_array.append(get_time(point['Timestamp']))
		data_array[0, index] = point['AngularX']
		data_array[1, index] = point['AngularY']
		data_array[2, index] = point['AngularZ']
	return sort_by_time(time_stamp_array, data_array)

def get_gsr_data(json_file_name):
	data_in=[]
	with open(json_file_name, 'r') as data_file:
		data_in = json.load(data_file)
	data_array = numpy.zeros((1, len(data_in)))
	time_stamp_array = []
	for index, point in enumerate(data_in):
		time_stamp_array.append(get_time(point['Timestamp']))
		data_array[0, index] = point['Resistance']
	return sort_by_time(time_stamp_array, data_array)

def get_skin_temp_data(json_file_name):
	data_in=[]
	with open(json_file_name, 'r') as data_file:
		data_in = json.load(data_file)
	data_array = numpy.zeros((1, len(data_in)))
	time_stamp_array = []
	for index, point in enumerate(data_in):
		time_stamp_array.append(get_time(point['Timestamp']))
		data_array[0, index] = point['Temperature']
	return sort_by_time(time_stamp_array, data_array)
