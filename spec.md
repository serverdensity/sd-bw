run on group
pick network interface

layout of the config file
{
	'email': 'h@email.com',
	'apikey': 'oenuthoenuth',
    'start': 'start-date',
    'end': 'end-date',
	'current_device': 'onetuhoneuth',
    'current_interface': 'eth0',
    'devices': [''],
    'interfaces': [''], # this may need to be a dictionary. 
    'type': 'rxMByteS'
}

API layout

how do I modify the config in a good way? Do I want to check several devices at the same time? It would be more api calls. 

sdbandwidth -d idhere > uses that device instead of the one in the config file

sdbandwidth -t start end > uses that time instead of the one in the config file. 

sdbandwidth -ad > all devices

sdbandwidth -n adapter > uses that network adapter instead of the one set in the config file. 

sdbandwitdh interfaces > returns a list of network interfaces available on the machine in shell, for the current device or for all the devices. Not sure. 

sdbandwidth devices > returns devices in shell (save them in config file)

sdbandwidth bandwidth -device_id -interface period > prints the bandwidth for given period. 

sdbandwidth emailme > adds a cronjob. 


bandwidth for period. 
mbit and megabyte -> convert to terabyte. gigabyte. 
config file. 

make a commandline application. 

make a cronjob that runs weekly. 

bonded network 

get available metrics
- see what ethernet things exist. 

list of 