#! /usr/bin/env python3
"""  
FileName: parse_message_details.py
Author: John Delgado
Created Date: 3/27/2021
Version: 1.0 Initial Development

This file gets the values appended by our client and then returns those values to the server
"""

def test_boolean(string_to_check):
    if string_to_check == 'True':
        return True

    elif string_to_check == 'False':
        return False

def parse_message_details(data):
    #we are appending 4 values to the end of the file, so we need to split the string into 5
    formatted_data = data.rsplit(';',5)

    message_dictionary = {
        "message_received":  formatted_data[0],
        "start_of_file":     test_boolean(formatted_data[1]),
        "file_name":         formatted_data[2],
        "end_of_file":       test_boolean(formatted_data[3]),
        "packet_size":       int(formatted_data[4])
    }

    return message_dictionary

    

