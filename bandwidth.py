import requests
import json
from collections import namedtuple

# need to figure out error handling. 

def available_metrics(config):
	try: 
		api_response = requests.get('https://api.serverdensity.io/metrics/definitions/{0}'.format(config['current_device']),
		    params={
		        'token': config['api_key'],
		        'start' : config['start'],
		        'end': config['end']
		    })
	except IndexError:
		pass

	return json.loads(api_response.text)

def available_devices(config):
	api_response = requests.get('https://api.serverdensity.io/inventory/devices', params = {
	        'token': config['api_key']
	    })
	return json.loads(api_response.text)

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


def bandwidth_response(config):
	"""Get total_bandwidth for current device and current interface"""
	config = read_config()

	filters = {
    'networkTraffic': {
        config['current_interface']: ['rxMByteS', 'txMByteS']
    	}
	}

	api_response = requests.get('https://api.serverdensity.io/metrics/graphs/{0}'.format(config['current_device']),
    	params={
	        'token': config['api_key'],
	        'start' : config['start'],
	        'end': config['end'],
	        'filter': json.dumps(filters)
	    })
	return json.loads(api_response.text)


config = read_config()

	
devices = available_devices(config)
metrics = available_metrics(config)
bandwidth = bandwidth_response(config)

device_names = get_devices(devices)
adapters = get_network_interfaces(metrics)
total_bandwidth = calculate_bandwidth(bandwidth)


