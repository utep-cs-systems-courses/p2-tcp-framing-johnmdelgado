#! /usr/bin/env python3
"""  
FileName: receive_line.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This will be in charge of receiving the line from the client. it takes in 1024 bytes at a time
until a 0 length read is read. Once a 0 length read is read, then the connection is closed
"""
from sys import stdin, stdout
from os import read, write, getenv
import socket
import sys


def receive_line(connection):
    connection.shutdown(socket.SHUT_WR)      # no more output
    while 1:
        data = connection.recv(1024).decode()
        if len(data) == 0:
            break
        else:            
            print("Received '%s'" % data)
    print("Zero length read.  Closing")
    connection.close()