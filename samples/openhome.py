#!/usr/bin/python
'''Exercising miscellanous OpenHome services and actions'''
from __future__ import print_function

import sys
import time
import xml.etree.ElementTree as ET
import upnpp

def debug(x):
   print("%s" % x, file = sys.stderr)
def usage():
   debug("Usage: getmedinfo.py devname")
   sys.exit(1)
   
if len(sys.argv) != 2:
   usage()
devname = sys.argv[1]

log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(2)

srv = upnpp.findTypedService(devname, "product", True)
if not srv:
   debug("'Product' service not found: device is not an openhome one")
   sys.exit(1)

retdata = upnpp.runaction(srv, "SourceCount", [])
sourcecount = int(retdata["Value"])
retdata = upnpp.runaction(srv, "SourceIndex", [])
sourceindex = int(retdata["Value"])

retdata = upnpp.runaction(srv, "SourceXml", [])
sourcexml = retdata["Value"]
# print("source count %d, source XML: %s" % (sourcecount, sourcexml))
xml = ET.XML(sourcexml)
sources = []
for child1 in xml:
   nm = ''
   tp = ''
   for child2 in child1:
      if child2.tag == 'Name':
         nm = child2.text
      elif child2.tag == 'Type':
         tp = child2.text
   sources.append((nm, tp))

if sourceindex < 0 or sourceindex >= len(sources):
   debug("No current source")
   sys.exit(1)

print("Current source name %s, type %s" % sources[sourceindex])

sourcetype = sources[sourceindex][1]
if sourcetype == "Playlist":
   srv = upnpp.findTypedService(devname, "playlist", True)
   if not srv:
      debug("findTypedService failed for playlist service")
      sys.exit(1)

   retdata = upnpp.runaction(srv, "Id", [])
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
