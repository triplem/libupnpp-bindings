#!/usr/bin/python3

import sys
import time
import upnpp
import re

ohpltype = "urn:av-openhome-org:service:Playlist"
avttype = "urn:schemas-upnp-org:service:AVTransport"

def beginsWith(s, beg):
   if s[0:len(beg)] == beg:
      return True
   return False

renderers = []
descriptions = upnpp.getDevices()

for dev in descriptions:
   print("Device: UDN: [%s] fname [%s]" % (dev.UDN, dev.friendlyName))
   print("  type: %s" % dev.deviceType)
   hasrenderer=False
   for srvdesc in dev.services:
      print ("  service: %s" % srvdesc.serviceType)
      if beginsWith(srvdesc.serviceType, avttype) or \
         beginsWith(srvdesc.serviceType, ohpltype):
         hasrenderer = True
      srvdesc.fetchAndParseDesc(dev.URLBase)
      for var in srvdesc.stateTable:
         print("    VARIABLE %s dataType %s" % (var.name, var.dataType))
      for act in srvdesc.actionList:
         print("    ACTION %s args:" % act.name)
         for arg in act.argList:
            print("      ARGUMENT %s" % arg.name)
   if hasrenderer:
      renderers.append(dev)

print("Renderers:")
for rdr in renderers:
   print("Renderer: %s" % rdr.friendlyName)
