import requests
import json


config = {
	'email': 'h@email.com',
	'start': '2014-11-10T10:00:00Z', # set this in the config file
	'end': '2014-11-10T18:00:00Z', # set in config file
	'current_device': '5460a47c76d377952c4420b3',
	'api_key': '5eefa2ed1f30d4f3d704100a591fbf73',
	'devices': [],
	'interfaces': [],
}

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
	pass


def total_bandwidth(config):
	"""Get total_bandwidth for current device and current interface"""
	config = read_config()

	filter = {
    'networkTraffic': {
        config['current_interface']: ['rxMByteS', 'txMByteS']
    	}
	}

	api_response = requests.get('https://api.serverdensity.io/metrics/graphs/{0}'.format(config['current_device']),
    	params={
	        'token': config['api_key'],
	        'start' : config['start'],
	        'end': config['end'],
	        'filter': json.dumps(filter)
	    })
	bandwidth_dic = calculate_bandwidth(json.loads(api_response.text))






	
devices = available_devices(config)
metrics = available_metrics(config)

device_names = get_devices(devices)
adapters = get_network_interfaces(metrics)


