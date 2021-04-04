#! /usr/bin/env python3

"""  
FileName: read_file.py
Author: John Delgado
Created Date: 3/27/2021
Version: 1.0 Initial Development

This is the main executeable file for the server
"""
from functions import get_config as gc
from functions import parse_message_details as pmd
from functions import server_file_opener as sfo
from os import write
import sys
import os
import socket

def receive_file(conn, addr):
    config = gc.get_config()

    #inialize variables from config file
    bytes_size = config["defaults"]["bytesToRead"]

    while 1:
        data = conn.recv(1024).decode()
        if len(data) == 0:
            print("Zero length read, nothing to send, terminating")
            break
        if len(data) == (bytes_size + 1):
            print("Larger packet than expected was received")
            break
        # break down the message with our appended message details
        message_details = pmd.parse_message_details(data)
        print(message_details)

        # check if start of file
        if message_details["start_of_file"]:
            print("This packet is the start of the file. We need to open a file descriptor using the name of file value to store the information")                                 
        file_descriptor = sfo.file_opener(message_details["file_name"])
        if len(data) < message_details["packet_size"]:
            # if the length of data is less than the expected packet size reach back out to client and say to 
            # resend data
            print("Packet size is less than expected. sending error to client to resend data.")
            send_message = "checksum failed. Resend failed packet"
        else:
            send_message = "Echoing %s" % message_details["message_received"]
        os.write(file_descriptor,message_details["message_received"].encode())
        print("Received '%s', sending '%s'" % (message_details["message_received"], send_message))
        while len(send_message):
            bytesSent = conn.send(send_message.encode())
            send_message = send_message[bytesSent:0]
        # if the end of the file has been received then we can close the file descriptor
        if message_details["end_of_file"]:
            print("End of file indicator received")
            os.close(file_descriptor)
            break              