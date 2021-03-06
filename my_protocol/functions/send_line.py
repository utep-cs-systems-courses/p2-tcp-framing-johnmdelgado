#! /usr/bin/env python3
"""  
FileName: send_line.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This will be in charge of sending the line to the server
"""
from sys import stdin, stdout
from os import read, write,getenv
import sys

def send_line(connection,messageToSend):
    while len(messageToSend):
        formatted_string = "sending string: {}\n".format(messageToSend)
        write(1,formatted_string.encode())
        bytesSent = connection.send(messageToSend.encode())
        messageToSend = messageToSend[bytesSent:]
