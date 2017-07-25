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

class EventReporter(object):
   def __init__(self, srv):
      debug("EventReporter.__init__")
      # This installs a reference from r to self
      self.r = upnpp.installReporter(srv, self)
   # Call this if you want this and the c++ object to be ever deleted
   # (else the self.r->self ref means the ref count will never go to 0
   def uninstall(self):
      del self.r
   def __del__(self):
      debug("EventReporter.__del__")
   def upnp_event(self, nm, value):
      print("%s -> %s" % (nm, ""))

r = EventReporter(srv)

for i in range(10):
   time.sleep(2)

r.uninstall()

