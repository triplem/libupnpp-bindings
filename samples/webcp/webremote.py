#!/usr/bin/python3
'''
Script to be used as with upmpdcli "onvolumechange" and "getexternalvolume"
configuration parameters. 
See webcp README for details.
'''

import subprocess
import json
import sys

#host = "localhost"
host = "192.168.4.4"

def _deb(x):
    print("%s" % x, file = sys.stderr)
def _usage():
    _deb("Usage: webremote host:port upnpdev service action [args]")
    sys.exit(1)
    
if len(sys.argv) < 5:
    _usage()

hostport = sys.argv[1]
dev = sys.argv[2]
serv = sys.argv[3]
act = sys.argv[4]

url = "http://%s/" % hostport
url += "?dev=%s&serv=%s&act=%s" % (dev, serv, act)

i = 1
for a in sys.argv[5:]:
    url += "&a" + str(i) + "=" + a
    i += 1

cmd = ["curl", "-s"]
cmd.append(url)
data = subprocess.check_output(cmd)

#_deb("URL: [%s]" % url)
#_deb("data: [%s]" % data)

json = json.loads(data)
if "Value" in json:
    print("%s" % json["Value"])
