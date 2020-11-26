#!/usr/bin/python3

import sys
import os
import upnpp
import time

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

srv = findservice(devname, "Playlist")
#runaction(srv, "Play", "")
upnpp.runaction(srv, "SeekId", ["24"])

srv = findservice(devname, "Info")

for actname, expected in (
        ("Counters", "DetailsCount MetatextCount TrackCount"),
        ("Track", "Metadata Uri"),
        ("Details", "BitDepth BitRate CodecName Duration Lossless SampleRate"),
        ("Metatext", "Value "),
        ):
    runaction(srv, actname, expected)

doloop=False
#doloop=True
while doloop:
    runaction(srv, "Details", "BitDepth BitRate CodecName Duration Lossless SampleRate")
    time.sleep(1)
    
printevents(srv)
