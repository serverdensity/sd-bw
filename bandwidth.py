import json
from collections import namedtuple
from urlparse import urljoin

import requests


# need to figure out error handling. 

BASE_URL = 'https://api.serverdensity.io'
CONFIG_PATH = '~/config.json'


def parse_response(response):
	try:
		data = json.loads(response.text)
	except ValueError:
		data = {}

	try:
		if response.status == 200:
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


def available_metrics(config):
	payload = {
		        'token': config['api_key'],
		        'start' : config['start'],
		        'end': config['end']
		    }

	api_response = get_jsondata('metrics/definitions/{0}'.format(config['current_device']), payload)

	return api_response

def bandwidth_response(config):
	"""Get total_bandwidth for current device and current interface"""

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

def available_devices(config):
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

def get_devices(devices):
	devicedic = {}
	for device in devices:
		devicedic[device['name']] =  device['_id']
	return devicedic

def read_config():
	config = {}
	with open('config.json', 'r') as f:
		config = json.load(f)
	return config

def modify_config(keydic):
	config = read_config()
	for key, val in keydic.iteritems():
		config[key] = val
	with open('config.json', 'w') as fp:
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





config = read_config()

	
devices = available_devices(config)
metrics = available_metrics(config)
bandwidth = bandwidth_response(config)

device_names = get_devices(devices)
adapters = get_network_interfaces(metrics)
total_bandwidth = calculate_bandwidth(bandwidth)


