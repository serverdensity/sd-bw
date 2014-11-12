import json
from collections import namedtuple
from urlparse import urljoin
import os.path

import requests


# need to figure out error handling. 

BASE_URL = 'https://api.serverdensity.io'
CONFIG_PATH = '~/.config.json'


def parse_response(response):
	try:
		data = json.loads(response.text)
	except ValueError:
		data = {}
	try:
		if response.status_code == 200:
			return data
		elif not data:
			data['message'] = 'Dictionary is empty'
			raise Exception
		elif response.status != 200:
			raise Exception
	except Exception:
		print 'Error: {0}'.format(data['message'])

def get_jsondata(urlpath, payload):
	response = requests.get(urljoin(BASE_URL, urlpath), params=payload)
	return parse_response(response)


def available_metrics():
	config = read_config()	
	payload = {
		        'token': config['api_key'],
		        'start' : config['start'],
		        'end': config['end']
		    }

	api_response = get_jsondata('metrics/definitions/{0}'.format(config['current_device']), payload)

	return api_response

def bandwidth_response():
	"""Get total_bandwidth for current device and current interface"""
	config = read_config()

	filters = {
    'networkTraffic': {
        config['current_interface']: ['rxMByteS', 'txMByteS']
    	}
	}

	payload = {
	        'token': config['api_key'],
	        'start' : config['start'],
	        'end': config['end'],
	        'filter': json.dumps(filters)
	    }

	api_response = get_jsondata('metrics/graphs/{0}'.format(config['current_device']), payload)

	return api_response

def available_devices():
	config = read_config()
	payload = {'token': config['api_key']}

	api_response = get_jsondata('/inventory/devices', payload)
	return api_response

def get_network_interfaces(metrics):
	"""Gives you a list of network adapters"""
	network = {}
	adapters = []
	for j in metrics:
		if j.get('key') == 'networkTraffic':
			network = j
			break

	for adapter in network['tree']:
		adapters.append(adapter['key'])

	return adapters

def get_groups(device_response):
	groupdic = {}
	for device in device_response:
		devicedic[device['group']] = { device['name']: device['_id']}
	return groupdic

def get_devices(device_response):
	devicedic = {}
	for device in device_response:
		devicedic[device['name']] =  device['_id']
	return devicedic

def present_devices():
	devices = available_devices()
	devicedic = get_devices(devices)

	for name, _id in devicedic.iteritems():
		print "Device: {0} 		ID: {1}".format(name, _id)


def read_config():
	config = {}
	try:
		with open(os.path.expanduser(CONFIG_PATH), 'r') as f:
			config = json.load(f)
	except IOError:
		print "Error: There is no config.json file"
	return config

def modify_config(keydic):
	config = read_config()
	for key, val in keydic.iteritems():
		config[key] = val
	with open(os.path.expanduser(CONFIG_PATH), 'w') as fp:
		json.dump(config, fp)

def calculate_bandwidth(trafficdic):
	rxmblist = trafficdic[0]['tree'][0]['tree'][0]['data']
	txmblist = trafficdic[0]['tree'][0]['tree'][1]['data']

	# There two definitions though
	# http://en.wikipedia.org/wiki/Gigabyte#Definition

	rxgb = sum([value['y'] for value in rxmblist])/1024
	txgb = sum([value['y'] for value in txmblist])/1024
	Bandwidth = namedtuple('Bandwidth', 'rxgb, txgb')

	return Bandwidth(rxgb, txgb)

if __name__ == '__main__':
	config = read_config()
	devices = available_devices()
	metrics = available_metrics()
	bandwidth = bandwidth_response()

	device_names = get_devices(devices)
	adapters = get_network_interfaces(metrics)
	total_bandwidth = calculate_bandwidth(bandwidth)


