#!/usr/bin/python3
'''Using the discovery service and the avtransport classes instead of
findTypedService(), and the string-based interface'''

import sys
import time
import upnpp

def debug(x):
   print("%s" % x, file = sys.stderr)

if len(sys.argv) != 2:
   usage()
def usage():
   debug("Usage: getmedinfo.py devname")
   sys.exit(1)
if len(sys.argv) != 2:
   usage()
fname = sys.argv[1]

log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(2)

# Get in touch with discovery service
dir = upnpp.UPnPDeviceDirectory_getTheDir()

# Retrieve device description for designated friendly name
#
# The weird approach is because the c++ method takes a reference
# to a description object, instead of returning a possibly null
# pointer to an allocated object (can't return a pointer to the
# original object because locking etc.). This avoid allocating a copy
# inside getDev...(), and deciding who is responsible for the memory.
description = upnpp.UPnPDeviceDesc()
if not dir.getDevByFName(fname, description):
   debug("%s not found" % fname)
   sys.exit(1)
   
# Find RenderingControl service description inside device, and create
# RenderingControl service. Again, a slightly strange approach: we
# want the class to look for an appropriate service description, and
# we use an empty object for this. This allows having only one helper
# in the .i file, instead of 1 per class if we were using the static
# methods. Another approach would be to have static methods in the
# C++, just taking an UDN or friendlyname, and returning an object.
rdrc = upnpp.RenderingControl()
status = rdrc.initFromDescription(description)
if status:
   vol = rdrc.getVolume()
   print("\nGOT rendering control service! Volume is %d" % vol)
else:
   debug("RenderingControl service not found")
   sys.exit(1)

avt = upnpp.AVTransport()
status = avt.initFromDescription(description)

if status:
   posinf = upnpp.AVTPositionInfo()
   status = upnpp.AVTGetPositionInfo(avt, posinf)
   print("PositionInfo: duration %d S, trackuri: %s" %
         (posinf.trackduration, posinf.trackuri))
