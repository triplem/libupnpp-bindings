#!/usr/bin/python

from __future__ import print_function

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
devices = upnpp.getDevices()

for dev in devices:
   print("Device: UDN: [%s] fname [%s]" % (dev.UDN, dev.friendlyName))
   print("  type: %s" % dev.deviceType)
   hasrenderer=False
   for service in dev.services:
      print ("  service: %s" % service.serviceType)
      if beginsWith(service.serviceType, avttype) or \
         beginsWith(service.serviceType, ohpltype):
         hasrenderer = True
      service.fetchAndParseDesc(dev.URLBase)
      for var in service.stateTable:
         print("    VARIABLE %s dataType %s" % (var.name, var.dataType))
      for act in service.actionList:
         print("    ACTION %s args:" % act.name)
         for arg in act.argList:
            print("      ARGUMENT %s" % arg.name)
   if hasrenderer:
      renderers.append(dev)

print("Renderers:")
for rdr in renderers:
   print("Renderer: %s" % rdr.friendlyName)
