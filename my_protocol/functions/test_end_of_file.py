#! /usr/bin/env python3
"""  
FileName: test_end_of_file.py
Author: John Delgado
Created Date: 3/7/2021
Version: 1.0 Initial Development

This will check a byte and determine if the end of file byte has been received
"""
from sys import stdin, stdout
from os import read, write,getenv
import sys

def test_end_of_file(string_to_check):
    #decode the byte and see if it is true or false
    if string_to_check[0] == "T":
        return True
    else:
        return False