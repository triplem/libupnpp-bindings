#!/usr/bin/python3
'''An HTTP service implementing a WEB "UPnP Control Point"
based on the python binding of libupnpp, see:
https://www.lesbonscomptes.com/upmpdcli/libupnpp-refdoc/libupnpp-ctl.html

The main / root entry point accepts  device, service, and action names, 
followed by optional parameters, and runs the action.

There is also a /devices entry point which will return an array of 
UDN,friendlyname pairs.

The output is json, so the other side must understand this.
'''

import os
import sys
import bottle
import upnpp
import json

def _deb(x):
    print("%s" % x, file = sys.stderr)

@bottle.route('/')
def main():
    args = []
    for item in bottle.request.query.iteritems():
        #_deb("item %s %s" % item)
        if item[0] == 'dev':
            dev = item[1]
        elif item[0] == 'serv':
            serv = item[1]
        elif item[0] == 'act':
            act = item[1]
        else:
            args.append(item[1])
    #_deb("device [%s] service [%s] action [%s]"%(dev,serv,act))
    srv = upnpp.findTypedService(dev, serv, True)
    if not srv:
        _deb("%s service not found: no device or not openhome" % serv)

    retdata = upnpp.runaction(srv, act, args)
    #_deb("main: type(retdata) %s" % type(retdata))
    return retdata

@bottle.route('/devices')
def listdevices():
    descriptions = upnpp.getDevices()
    alldevices = []
    for dev in descriptions:
        alldevices.append((dev.UDN, dev.friendlyName))
    return json.dumps(alldevices)
