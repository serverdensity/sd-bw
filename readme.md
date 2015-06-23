# SDBW CLI
-----------

**sdbw** is a command line interface for [Server Density](http://www.serverdensity.com) that shows and aggregates the bandwidth usage for a group or a device.

## Installation
-----------------
`$ pip install sd-bandwidth`

## Usage
---------
```
$ sdbw -h
CLI for checking bandwidth at Server Density.

Usage:
        sdbw groups (update | view)
        sdbw devices (update | view)
        sdbw bandwidth (group <name> | -g <name>) [(-t <start> <end>)]
        sdbw bandwidth (device <name> | -d <name>) [(-t <start> <end>)]
        sdbw time (set (<start> <end>) | view)
        sdbw -h | --help
        sdbw -v | --version

Options:
        -d <name>               Use this device name to check bandwidth
        -g <name>               Use this group name to check bandwidth
        -t <start> <end>        Use this time and update time in config: YYYY-MM-DDTHH:MM:SSZ
        -v, --version           Show version
        -h, --help              Show help
```

## Authentication
------------------

The first time you use the application an authentication prompt will automatically show up. Input an [API token](https://apidocs.serverdensity.com/API_Basics/Getting_Started) and you'll be good to go. 

    You need an authentication token
    What is your token: 12345678aoeuidhtn
    Token verified.

The token is saved in a `.config.json` in your home directory. 

## Time 
-------

You can either set the time with the following command
    
    sdbw time set YY-MM-DDTHH:MM:SSZ YY-MM-DDTHH:MM:SSZ 

or using the flag `-t`. Either way, the time that was last input will be saved in the config file. 


 
