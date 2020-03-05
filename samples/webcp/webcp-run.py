#!/usr/bin/python3
import os
import argparse
import webcp

# handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--addr', default='127.0.0.1',
                    help='address to bind to [127.0.0.1]')
parser.add_argument('-p', '--port', default='9090', type=int,
                    help='port to listen on [9090]')
args = parser.parse_args()

# set up and run in own http server
webcp.bottle.debug(False)
webcp.bottle.run(host=args.addr, port=args.port, reloader=False)
