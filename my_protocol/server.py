#! /usr/bin/env python3

"""  
FileName: server.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This is the main executeable file for the server
"""
from functions import get_config as gc
from os import write
import sys
import os
import socket
if __name__ == '__main__':
    print("Starting server.....")
    print("Reading configuration file...")

    config = gc.get_config()
    print("Configuration file successfully read")

    #inialize variables from config file
    listenPort = config["serverDefaults"]["listenPort"]
    usage = config["serverDefaults"]["usage"]
    listenAddr = config["serverDefaults"]["listenAddress"]
    bytes_size = config["defaults"]["bytesToRead"]

    print("listening on port: {}".format(listenPort))
    print("useage is set to: {}".format(usage))
    print("packet size set to: {}".format(bytes_size))
    print("Server started")
    print("Starting listener....") 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listenAddr, listenPort))
    s.listen(1)              # allow only one outstanding request
    # s is a factory for connected sockets

    print("Listener Started")

    while 1:
        print("listening...")
        conn, addr = s.accept()  # wait until incoming connection request (and accept it)
        print('Connected by', addr)
        while 1:
            data = conn.recv(1024).decode()
            if len(data) == 0:
                print("Zero length read, nothing to send, terminating")
                break
            if len(data) == (bytes_size + 1):
                print("End of file has been received.")
                break
            sendMsg = "Echoing %s" % data
            print("Received '%s', sending '%s'" % (data, sendMsg))
            while len(sendMsg):
                bytesSent = conn.send(sendMsg.encode())
                sendMsg = sendMsg[bytesSent:0]
        conn.shutdown(socket.SHUT_WR)
        conn.close()
