#!/usr/bin/python

from __future__ import print_function

import sys
import time
import upnpp

def debug(x):
   print("%s" % x, file = sys.stderr)

def runaction(srv, action, args, retdata):
   ret = srv.runAction(action, args, retdata)
   if ret:
      debug("%s failed with %d" % (action, ret))
   else:
      debug("%s succeeded" % action)
      if len(retdata) != 0:
         debug("Got data:")
         for nm, val in retdata.iteritems():
            debug("    %s : %s" % (nm, val))
   return ret
   
srv = upnpp.findTypedService("UpMpd-r31", "avtransport", True)

if not srv:
   debug("findTypedService failed")
   sys.exit(1)

args = upnpp.VectorString()
retdata = upnpp.MapStringString()

args.append("0")

while True:
    runaction(srv, "GetMediaInfo", args, retdata)
    time.sleep(2)

