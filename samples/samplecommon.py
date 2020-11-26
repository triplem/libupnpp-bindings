import upnpp
import sys
import time

def debug(x):
    print("%s" % x, file = sys.stderr)

def findservice(devname, servicename):
    srv = upnpp.findTypedService(devname, servicename, True)
    if not srv:
        debug("'%s' service not found" % servicename)
        sys.exit(1)
    return srv

def runsimpleaction(srv, actname, expected):
    print("Running [%s] action. Expected: [%s]" % (actname, expected))
    elist = expected.split()
    data = upnpp.runaction(srv, actname, [])
    for nm in elist:
        if not nm in data:
            debug("Missing [%s] element in response" % nm)
            sys.exit(1)
    for nm, val in data.items():
        print("%s -> %s" % (nm, val))
    print("")
    return data

def printevents(srv):
    print("\nEvents:")
    class EventReporter:
        def upnp_event(self, nm, value):
            print("%s -> %s" % (nm, value))
    reporter = EventReporter()
    bridge = upnpp.installReporter(srv, reporter)
    while True:
        time.sleep(20000)
    
