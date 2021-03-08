#! /usr/bin/env python3

"""  
FileName: server.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This is the main executeable file for the server
"""
from functions import get_config as gc
from functions import test_end_of_file as eof
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
    whole_file = ""
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
                print("Larger packet than expected was received")
                break                                 
            message_recevied = data.rsplit(';',1)[0]
            packet_infomation = (data.rsplit(';',1)[1]).strip()
            end_of_file_ind = (packet_infomation.split('e')[0]).strip()
            packet_size = int((packet_infomation.split('e')[1]).strip())
            # check the second to last byte of the received data for end of file ind
            test_eof = eof.test_end_of_file(end_of_file_ind)
            print("eof is: {}\n".format(test_eof))
            # check last byte of packet for packet size
            print("packet size is: {}\n".format(packet_size))
            # remove values from byte array
            if len(data) < packet_size:
                # if the length of data is less than the expected packet size reach back out to client and say to 
                # resend data
                print("Packet size is less than expected. sending error to client to resend data.")
                send_message = "checksum failed. Resend failed packet"
            else:
                send_message = "Echoing %s" % message_recevied
            whole_file += message_recevied
            print("Received '%s', sending '%s'" % (message_recevied, send_message))
            while len(send_message):
                bytesSent = conn.send(send_message.encode())
                send_message = send_message[bytesSent:0]
            if test_eof:
                print("End of file indicator received")
                print("whole file is:")
                print(whole_file)                
                whole_file= ""
                break                
            
        conn.shutdown(socket.SHUT_WR)
        conn.close()

