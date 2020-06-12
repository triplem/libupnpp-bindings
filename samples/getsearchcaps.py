#!/usr/bin/python3

import sys
import time
import upnpp

def debug(x):
   print("%s" % x, file = sys.stderr)
def usage():
   debug("Usage: getmedinfo.py devname")
   sys.exit(1)
   
if len(sys.argv) != 2:
   usage()
devname = sys.argv[1]

srv = upnpp.findTypedService(devname, "contentdirectory", True)

if not srv:
   debug("findTypedService failed")
   sys.exit(1)

retdata = upnpp.runaction(srv, "GetSearchCapabilities", [])

for nm,val in retdata.items():
   print("%s: %s" % (nm, val))
   
