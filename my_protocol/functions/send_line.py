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

def send_line(connection,message_to_send,start_of_file,file_name,end_of_file,packet_size):
    while len(message_to_send):
        formatted_string = "sending string: {}\n".format(message_to_send)
        write(1,formatted_string.encode())
        message_to_send = "{};{};{};{};{}".format(message_to_send,start_of_file,file_name,end_of_file, packet_size)
        bytesSent = connection.send(message_to_send.encode())
        message_to_send = message_to_send[bytesSent:]
