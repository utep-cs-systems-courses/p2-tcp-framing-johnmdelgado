#! /usr/bin/env python3

"""  
FileName: server.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This is the main executeable file for the server
"""
from functions import get_config as gc
from functions import parse_message_details as pmd
from functions import server_file_opener as sfo
from functions import test_in_transfer as it
from os import write
import sys
import os
import socket
import threading
import queue

class myThread (threading.Thread):
   def __init__(self, threadID, name, addr,conn, queue):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.addr = addr
      self.conn = conn
      self.queue = queue

   def run(self):
      print("Starting " + self.name)
      #print("trying test process data")
      #process_data(self.name, self.queue)
      print("trying to process message")
      process_message(self.name,self.queue, self.addr, self.conn)
      print("Exiting " + self.name)

def process_data(threadName, queue):
    transfer_lock.acquire()

    if not work_queue.empty():
        data = queue.get()
        transfer_lock.release()
        print("whoa this is in the test test thread!%s processing %s" % (threadName, data))
    else:
        transfer_lock.release()
        print("releasing lock")

def process_message(thread_name, queue,conn,addr):
    print("aquiring lock for: {}".format(thread_name))
    transfer_lock.acquire()
    print("here is the work queue:")
    for q in work_queue:
        print(q)

    if not work_queue.empty():
        data = queue.get()
        transfer_lock.release()
        print("%s processing %s" % (thread_name, data))

        while 1:
            conn.recv(1024).decode()
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

            if len(data) < message_details["packet_size"]:
                # if the length of data is less than the expected packet size reach back out to client and say to 
                # resend data
                print("Packet size is less than expected. sending error to client to resend data.")
                send_message = "checksum failed. Resend failed packet"

            # check if file is already in the process of being transferred
            # elif it.test_in_transfer(message_details["file_name"]):
            #     print("This file is currently in process and can not be received right now")
            #     send_message = "This file is currently in process and can not be received right now"

            # if not in transfer and the packet size is expected, open the file and write to it 
            else:
                send_message = "Echoing %s" % message_details["message_received"]
                file_descriptor = sfo.file_opener(message_details["file_name"])
                os.write(file_descriptor,message_details["message_received"].encode())

            print("Received '%s', sending '%s'" % (message_details["message_received"], send_message))
            while len(send_message):
                bytesSent = conn.send(send_message.encode())
                send_message = send_message[bytesSent:0]
            # if the end of the file has been received then we can close the file descriptor
            if message_details["end_of_file"]:
                print("End of file indicator received")
                in_transfer_threads.remove(message_details["file_name"])
                os.close(file_descriptor)
                break
        conn.shutdown(socket.SHUT_WR)
        conn.close()
    else:
        transfer_lock.release()
        print("releasing lock")

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
    # initilize threading set
    transfer_lock = threading.Lock()
    in_transfer_threads = set() 
    work_queue = queue.Queue()
    thread_id = 1

    print("Listener Started")
    while 1:
        print("listening...")
        conn, addr = s.accept()  # wait until incoming connection request (and accept it)
        thread_name = "thread#{}".format(thread_id)
        print('Connected by: {}. Starting new thread: {}.'.format(addr,thread_name))
        thread = myThread(thread_id,thread_name,addr,conn,work_queue)
        thread.start()
        in_transfer_threads.add(thread)
        thread_id += 1

        print("Here is the current thread info: {}".format(thread))
        print("Here is the thread queue: {}".format(in_transfer_threads))

        #Add to the queue
        transfer_lock.acquire()
        work_queue.put(thread)
        transfer_lock.release()

        #wait for the queue to empty
        while not work_queue.empty():
            pass

        # Wait for all threads to complete
        for thread in in_transfer_threads:
            thread.join()

        print("all threads completed!")


        #process_message(in_transfer_threads,conn,addr)

