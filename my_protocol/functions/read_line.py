#! /usr/bin/env python3
"""  
FileName: my_get_line.py
Author: John Delgado
Created Date: 2/7/2021
Version: 1.0 Initial Development

This will utilize the my_get_char buffer and interprete the buffer and print out each line from the buffer.
If the string is too long for the buffer, then it will refresh the buffer, until a new line character is detected.
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

        
def read_line(bytes_size,debug):
    prompt = get_prompt()
    write(1, prompt.encode())
    read_from_buffer = gc.get_char(bytes_size,debug)
    if debug:
        formatted_string = "This is the current buffer:\n {}".format(read_from_buffer)
        write(2,formatted_string.encode())
    index = 0
    whole_line = ""
    while index < len(read_from_buffer):
        character = read_from_buffer[index]
        if debug:
            write(2,("Current Character: [{}]".format(character)).encode())     
        # if a new line character is dectected Evaluate the line and see if it is a command    
        if (character == "\n"):
            if debug:
                write(2,"New line detected".encode())
            write(2, ("{}\n".format(whole_line)).encode())
            #connection = cc.new_connection()
            #sl.send_line(connection,whole_line)
            #rl.receive_line(connection)
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
            sl.send_line(connection,read_from_buffer)
            rl.receive_line(connection)
            formatted_string = "sending {} bytes".format(bytes_size)
            write(1, formatted_string.encode())
            test_buffer = gc.get_char(bytes_size,debug)
            if len(test_buffer) == 0 :
                # if nothing is left in the buffer, then we can send a message to the server saying we are done
                # this file will be a n+1 byte size file because our reader only reads n bytes at a time, by sending
                # a byte string that is n+1 our server will know that we are finished sending.
                write(2,"nothing left in the buffer!!\n".encode())
                size = (bytes_size + 1)                
                formatted_string = "sending n+1({}) bytes terminating array\n".format(size)
                write(1, formatted_string.encode())
                nplus1array = bytearray(size).decode()
                connection.close()
                connection = cc.new_connection()
                sl.send_line(connection,nplus1array)
                rl.receive_line(connection)
                sys.exit(0)
            else:
                read_from_buffer = test_buffer
                index = 0
                continue

        index += 1