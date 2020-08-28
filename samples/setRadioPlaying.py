#!/usr/bin/python3

import sys
import time
from lxml import etree
# from io import StringIO
import upnpp

# Set this
devname = "upmpd-bureau"
radiotitle = "Radio Paradise (flac)"

def debug(x):
   print("%s" % x, file = sys.stderr)
   
log = upnpp.Logger_getTheLog("stderr")
log.setLogLevel(2)

srv = upnpp.findTypedService(devname, "product", True)
if not srv:
   debug("'Product' service not found: device %s is not openhome or not found" %
         devname)
   sys.exit(1)

retdata = upnpp.runaction(srv, "SetSourceIndexByName", ["Radio"])

srv = upnpp.findTypedService(devname, "radio", True)
if not srv:
   debug("'radio' service not found")
   sys.exit(1)
retdata = upnpp.runaction(srv, "ChannelsMax", [])
chanmax = int(retdata["Value"])

ifound = -1
uri = ""

# We should read and decode the idarray, but we happen to know that
# upmpdcli ids are 0-max
for i in range(chanmax):
   if ifound != -1:
      break
   retdata = upnpp.runaction(srv, "Read", [str(i)])
   debug("%s"%retdata)
   root = etree.fromstring(retdata["Metadata"])
   for child1 in root:
      for child2 in child1:
         if child2.tag.endswith("res"):
            if child2.text is not None:
               uri = child2.text
         if child2.tag.endswith("title") and child2.text == radiotitle:
            ifound = i

if ifound == -1:
   print("Channel <%s> not found"%radiotitle, file=sys.stderr)
   sys.exit(1)

upnpp.runaction(srv, "SetId", [str(ifound), uri])
upnpp.runaction(srv, "Play", [])
sys.exit(0)
