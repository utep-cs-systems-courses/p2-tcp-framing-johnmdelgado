#! /usr/bin/env python3
"""  
FileName: my_get_line.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This will utilize the my_get_char buffer and interprete the buffer and print out each line from the buffer.
If the string is too long for the buffer, then it will refresh the buffer, until a new line character is detected.
at the end of the buffer, the buffer is sent to our server client. 
This code was based off of project 1. Please see resources section of readme.md
"""
from sys import stdin, stdout
from functions import get_char as gc
from functions import send_line as sl
from functions import create_connection as cc
from functions import receive_line as rl 
from os import read, write,getenv
import sys

def get_prompt():
    prompt = getenv('PS1')
    if prompt is None:
        prompt = "$"
    prompt_format = "{} ".format(prompt)
    return prompt_format

        
def read_line(bytes_size,file_name,debug):
    prompt = get_prompt()
    write(1, prompt.encode())
    read_from_buffer = gc.get_char(bytes_size,debug)
    if debug:
        formatted_string = "This is the current buffer:\n {}".format(read_from_buffer)
        write(2,formatted_string.encode())
    index = 0
    whole_line = ""
    start_of_file = True
    while index < len(read_from_buffer):
        character = read_from_buffer[index]
        if debug:
            write(2,("Current Character: [{}]".format(character)).encode())     
        # if a new line character is dectected Evaluate the line and see if it is a command    
        if (character == "\n"):
            if debug:
                write(2,"New line detected".encode())
            write(2, ("{}\n".format(whole_line)).encode())
            connection = cc.new_connection()
            sl.send_line(connection,read_from_buffer,True,file_name,True,len(read_from_buffer))
            rl.receive_line(connection)
            whole_line =""
            write(1, prompt.encode())

        # If those conditions have not been met, then add the current character to our string        
        else: 
            whole_line += character

        # if we've reached the end of the buffer and a new line character has not been detected
        # then we need to read in another 100 bytes from the buffer
        # but we also need to add the current character to the string
        if index == (len(read_from_buffer)-1):
            # If we're about to reach the end of our buffer of n bytes, go ahead and send what we have
            # first send a message to the server saying to start listening for the entire message
            #
            connection = cc.new_connection()
            test_buffer = gc.get_char(bytes_size,debug)
            end_of_file = False
            if len(test_buffer) == 0 :
                # if nothing is left in the buffer, then we can send a message to the server saying we are done
                # this file will be a n+1 byte size file because our reader only reads n bytes at a time, by sending
                # a byte string that is n+1 our server will know that we are finished sending.
                write(2,"nothing left in the buffer!!\n".encode())
                end_of_file = True
            
            sl.send_line(connection,read_from_buffer,start_of_file,file_name,end_of_file,len(read_from_buffer))
            rl.receive_line(connection)
            formatted_string = "sending {} bytes\n".format(len(read_from_buffer))
            write(1, formatted_string.encode())                
            if end_of_file:
                sys.exit(0)
            read_from_buffer = test_buffer
            index = 0
            start_of_file = False
            continue
        index += 1
