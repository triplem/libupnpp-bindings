#!/usr/bin/python
from __future__ import print_function

import sys
import time
import upnpp
import random

verbose = False
superverbose = False
nruns = 10

url1 = "http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/mp3rates/mp3-064.mp3"
url2 = "http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/mp3rates/mp3-192.mp3"
seekpoint = "0:0:5"
duration = 5

url1 = "http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/mp3cbrmozart/01-Violin_Concerto_in_A_minor,_BWV_1041__I._Allegro_moderato.flac"
url2 = "http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/mp3cbrmozart/01-VCAM-64cbr.mp3"
seekpoint = "0:0:2"
duration = 3

#url1="http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/archimago-mqa/01*20-*20Arnesen*20A.flac"
#url2="http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/archimago-mqa/02*20-*20Arnesen*20B.flac"
#seekpoint = "0:0:5"
#duration = 5

#url1="http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/archimago-mqa/05*20-*20Mozart*20A.flac"
#url2="http://192.168.4.4:9790/minimserver/*/mp3/test-tracks/archimago-mqa/06*20-*20Mozart*20B.flac"
#seekpoint = "0:1:28"
#duration = 10

random.seed()
results = []

def debug(x):
   print("%s" % x, file = sys.stderr)

def runaction(srv, action, args, retdata):
   ret = srv.runAction(action, args, retdata)
   if ret:
      debug("%s failed with %d" % (action, ret))
   else:
      if superverbose:
         debug("%s succeeded" % action)
      if len(retdata) != 0 and superverbose:
         debug("Got data:")
         for nm, val in retdata.iteritems():
            debug("    %s : %s" % (nm, val))
   return ret
   
renderer = "UpMpd-r31"

srv = upnpp.findTypedService(renderer, "avtransport", True)
if not srv:
   debug("findTypedService failed")
   sys.exit(1)
   
args = upnpp.VectorString()
retdata = upnpp.MapStringString()

args_track1 = ["0", url1, ""]
args_track2 = ["0", url2, ""]

def playone(tpargs):
   runaction(srv, "SetAVTransportURI", tpargs, retdata)
   args = ["0", "1"] # Instanceid speed
   runaction(srv, "Play", args, retdata)
   if seekpoint != "0:0:0":
      args = ["0", "REL_TIME", seekpoint] # InstanceId, Unit, target
      runaction(srv, "Seek", args, retdata)
   if verbose:
      args = ["0"]
      runaction(srv, "GetMediaInfo", args, retdata)
      debug("URL: %s" % retdata["CurrentURI"])

   time.sleep(duration)
   args = ["0"]
   runaction(srv, "Stop", args, retdata)
   
for i in range(nruns):
   # trackorder = random.choice((0,1)) It actually does not seem a
   # good idea to switch a/b because it makes things more
   # difficult. Probably the best approach would be to re-run the
   # whole seq with a/b switched? or do 5+5
   trackorder = 1
   if trackorder:
      myargs1 = args_track1
      myargs2 = args_track2
   else:
      myargs1 = args_track2
      myargs2 = args_track1

   print("Playing A")
   playone(myargs1)
   time.sleep(1)
   
   print("Playing B")
   playone(myargs2)
   time.sleep(1)

   x = random.choice((0,1))
   if x:
      args = myargs2
   else:
      args = myargs1
   print("Playing X")
   playone(args)

   answer = ''
   while answer not in ('A', 'a', 'B', 'b'):
      answer = raw_input("Enter result (A/B): ")

   if answer in ('A', 'a'):
      if x:
         results.append(0)
      else:
         results.append(1)
   elif answer in ('B', 'b'):
      if x:
         results.append(1)
      else:
         results.append(0)


debug("%s"%results)
