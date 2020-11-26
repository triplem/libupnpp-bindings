#!/usr/bin/python3
'''Exercising miscellanous OpenHome services and actions'''

import sys
import os
import time
import xml.etree.ElementTree as ET
import upnpp
from samplecommon import debug as debug
from samplecommon import findservice as findservice
from samplecommon import runsimpleaction as runaction
from samplecommon import printevents as printevents

def usage():
    prog = os.path.basename(__file__)
    debug("Usage: %s devname" % prog)
    sys.exit(1)
   
if len(sys.argv) != 2:
   usage()
devname = sys.argv[1]

log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(2)

srv = findservice(devname, "product")

print("Exercising Product service:")
runaction(srv, "Product", "ImageUri Info Name Room Url")
runaction(srv, "Model", "ImageUri Info Name Url")
runaction(srv, "Attributes", "Value")
#retdata = upnpp.runaction(srv, "SetStandby", ["false"])
#print("setstandby answer:[%s]" % retdata)
runaction(srv, "SourceCount", "Value")
data = runaction(srv, "SourceIndex", "Value")
sourceindex = int(data["Value"])
data = runaction(srv, "SourceXml", "Value")
sourcexml = data["Value"]
data = upnpp.runaction(srv, "SetStandby", ["false"])
print("SetStandby return [%s]" % data)

xml = ET.XML(sourcexml)
sources = []
for child1 in xml:
   nm = ''
   snm = ''
   tp = ''
   for child2 in child1:
      if child2.tag == 'Name':
         nm = child2.text
      if child2.tag == 'SystemName':
         snm = child2.text
      elif child2.tag == 'Type':
         tp = child2.text
   sources.append((nm, snm, tp))

if sourceindex < 0 or sourceindex >= len(sources):
   debug("No current source")
   sys.exit(1)

print("Current source name %s, systemName %s type %s" % sources[sourceindex])

sourcetype = sources[sourceindex][1]
if sourcetype == "Playlist":
   srv = findservice(devname, "playlist")
   retdata = runaction(srv, "Id", "Value")
   if not retdata:
      sys.exit(1)
   id = retdata["Value"]
   print("Id: %s" % id)
   if id == "0":
      debug("No current track")
      sys.exit(1)
   retdata = upnpp.runaction(srv, "Read", [retdata["Value"]])
   if not retdata:
      sys.exit(1)
   metadata = retdata["Metadata"]
elif sourcetype == "Radio":
   srv = upnpp.findTypedService(devname, "radio", True)
   if not srv:
      debug("findTypedService failed for Radio service")
      sys.exit(1)

   retdata = upnpp.runaction(srv, "Channel", [])
   if not retdata:
      sys.exit(1)
   metadata = retdata["Metadata"]
else:
   debug("Can't do a thing with source type %s" % sourcetype)
   sys.exit(1)
   
if metadata:
   print("\nParsed metadata:")

   dirc = upnpp.UPnPDirContent()
   dirc.parse(metadata)

   if dirc.m_items.size():
      dirobj = dirc.m_items[0]
      print("  title: %s "% dirobj.m_title)
      for nm, val in dirobj.m_props.iteritems():
         print("  %s : %s" % (nm, val))

      resources = dirobj.m_resources
      if len(resources):
         print("Resource object details:")
         for nm, val in resources[0].m_props.iteritems():
            print("  %s : %s" % (nm, val))
