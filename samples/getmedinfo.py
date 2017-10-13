#!/usr/bin/python

from __future__ import print_function

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

srv = upnpp.findTypedService(devname, "avtransport", True)

if not srv:
   debug("findTypedService failed")
   sys.exit(1)

retdata = upnpp.runaction(srv, "GetMediaInfo", ["0"])

metadata = retdata["CurrentURIMetaData"]
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
   
