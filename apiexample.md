bandwidth = [{
	u 'name': u 'Network traffic', 
	u 'key': u 'networkTraffic',
    u 'tree': [{
    	u 'name': u 'eth0',
        u 'tree': [{
        	u 'name': u 'Received MB/s', 
        	u 'unit': u 'MB/s',
            u 'data': [ {
                u 'y': 9.765625e-05, u 'x': 1415642282
            }, {
                u 'y': 9.765625e-05, u 'x': 1415642347
            }], 
        }, {
        	u 'name': u 'Transmitted MB/s', 
        	u 'unit': u 'MB/s',
            u 'data': [ {
                u 'y': 0.000537109375, u 'x': 1415642282
            }, {
                u 'y': 0.000537109375, u 'x': 1415642347
            }], 
        }], 
    }]
}]

# Reality
----------

bandwidth[0]['tree'][0]['tree'][0][data]
When the api looks like this there is a cognitive load when writing programs for it. Then if you read the code it says nothing about what this bandwidth object really contains. 


# Ideal
--------

Either I would like to have the tree levels to keep separation. Or I would remove the tree levels as well. What are the downsides of this approach. Even if you wanted to change the api, it's not something that comes easily since we already have users of it. 

## Example

bandwidth['networkTraffic']

'name'
'tree'

bandwidth['networkTraffic']['tree']

'eth0'
'other interfaces'

bandwidth['networkTraffic']['tree']['eth0']

'tree' 

bandwidth['networkTraffic']['tree']['eth0']['tree']

'rxMByteS'
'txMByteS'

bandwidth['networkTraffic']['tree']['eth0']['tree']['rxMByteS']

'name'
'unit'
'data' <- list!