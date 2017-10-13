#!/usr/bin/python

from __future__ import print_function

import sys
import time
import upnpp

def debug(x):
   print("%s" % x, file = sys.stderr)

srv = upnpp.findTypedService("UpMpd-bureau", "avtransport", True)

if not srv:
   debug("findTypedService failed")
   sys.exit(1)
   
args = ["0", "http://192.168.4.4:9790/minimserver/*/mp3/variete/billy_joel/the_stranger/01*20-*20Movin*27*20Out*20(Anthony*27s*20Song).mp3", ""]
# retdata = upnpp.runaction(srv, "SetAVTransportURI", args)

# Instanceid speed
# retdata = upnpp.runaction(srv, "Play", ["0", "1"])

def seekloop():
   for i in range(0,3):
      # InstanceId, Unit, target
      retdata = upnpp.runaction(srv, "Seek", ["0", "REL_TIME", "0:0:30"])
      retdata = upnpp.runaction(srv, "GetMediaInfo", ["0"])
      time.sleep(2)

#retdata = upnpp.runaction(srv, "Seek", ["0", "REL_TIME", "0:20:30"])


retdata = upnpp.runaction(srv, "GetPositionInfo", ["0"])

retdata = upnpp.runaction(srv, "Stop", ["0"])


# Get in touch with discovery service
dir = upnpp.UPnPDeviceDirectory_getTheDir()

# Retrieve device description for designated friendly name
#
# The weird approach is because the c++ method takes a reference
# to a description object, instead of returning a possibly null
# pointer to an allocated object (can't return a pointer to the
# original object because locking etc.). This avoid allocating a copy
# inside getDev...(), and deciding who is responsible for the memory.
fname = "UpMpd-bureau"
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
# rdr = RenderingControlFindAllocate(friendlyname)
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
   print("\nAVTRansport ok: PositionInfo: trackuri: %s" % posinf.trackuri)
   
