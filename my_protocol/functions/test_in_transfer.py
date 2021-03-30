#! /usr/bin/env python3
"""  
FileName: test_in_transfer.py
Author: John Delgado
Created Date: 3/27/2021
Version: 1.0 Initial Development

This file is checking if the file being accepted is currently in the process of transfering
"""

def test_in_transfer(in_transfer, file_name):
    if file_name in in_transfer:
        return True

    else:
        return False