#!/usr/bin/python3
#
# Connect to a device/service and print all events.
#

import sys
import time
import upnpp

def msg(x):
   print("%s" % x, file = sys.stderr)
def usage():
   msg(
      "Usage: events.py <device> <service>\n" \
      "Sample script: will sleep forever, printing events from the " \
      "specified \n    renderer and service\n"
      " renderer can be specified as a case-insensitive friendly name or "
      "an exact UUID\n"
      " service can be partially specified (case-insensitive substring " \
      "match \n  in the actual service strings)\n"
      "Example: events.py myrenderer avtransport")
   sys.exit(1)
   

if len(sys.argv) != 3:
   usage()
devname = sys.argv[1]
fuzzyservicename = sys.argv[2]


srv = upnpp.findTypedService(devname, fuzzyservicename, True)
if not srv:
    msg("findTypedService failed")
    sys.exit(1)


# If the event reporter object holds a ref to the bridge class nobody
# ever gets deleted (because of circular reference) except if we
# explicitly call uninstall . This makes things more complicated.
def bridgeref_reporter_nogood():
   class EventReporter(object):
      def __init__(self, srv):
         # This installs a reference from r to self
         self.r = upnpp.installReporter(srv, self)

      # Call this if you want this and the c++ object to be ever deleted
      # (else the self.r->self ref means the ref count will never go to 0)
      def uninstall(self):
         del self.r

      def upnp_event(self, nm, value):
         print("%s -> %s" % (nm, value))

   reporter = EventReporter(srv)
   time.sleep(4)
   reporter.uninstall()



# Do this instead: separate storage of the callback and bridge
class EventReporter:
   def upnp_event(self, nm, value):
      print("%s -> %s" % (nm, value))

reporter = EventReporter()

# You do need to store the result of installReporter
bridge = upnpp.installReporter(srv, reporter)

while True:
   time.sleep(20000)
