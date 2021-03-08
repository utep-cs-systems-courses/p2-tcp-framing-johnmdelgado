#! /usr/bin/env python3
"""  
FileName: send_line.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This will be in charge of creating a connection to the server
"""
from functions import get_config as mc
from os import read, write,getenv
import socket, sys, re
import sys

def new_connection():
    #read in config to get server port
    config = mc.get_config()
    server = config["clientDefaults"]["serverPort"]
    usage  = config["clientDefaults"]["usage"]
  
    if usage:
        write(2,"Usage is enabled")
        #params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    socket_info = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            socket_info = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            socket_info = None
            continue
        try:
            print(" attempting to connect to %s" % repr(sa))
            socket_info.connect(sa)
            return socket_info
        except socket.error as msg:
            print(" error: %s" % msg)
            socket_info.close()
            socket_info = None
            continue
        break

    if socket_info is None:
        print('could not open socket')
        sys.exit(1)