#!/usr/bin/python3

import sys
import os
import upnpp

def debug(x):
    print("%s" % x, file = sys.stderr)
def usage():
    prog = os.path.basename(__file__)
    debug("Usage: %s devname" % prog)
    sys.exit(1)
   
if len(sys.argv) != 2:
    usage()
devname = sys.argv[1]

log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(2)

servicename = "credentials"
srv = upnpp.findTypedService(devname, servicename, True)
if not srv:
    debug("'%s' service not found: device is not an openhome one" % servicename)
    sys.exit(1)

data = upnpp.runaction(srv, "Get", ['qobuz'])

for nm, val in data.items():
    print("%s -> %s" % (nm, val))

