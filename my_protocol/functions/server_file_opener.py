#! /usr/bin/env python3
"""  
FileName: server_file_opener.py
Author: John Delgado
Created Date: 3/27/2021
Version: 1.0 Initial Development

This file creates/opens a file at the configured path in the config file using the file name provided
"""

from functions import get_config as mc
import os

def file_opener(file_name):
    #read in config to get default transfer path
    config = mc.get_config()

    #get the default file path and then append the file name to the end
    formatted_file_path = "{}{}".format(config["serverDefaults"]["downloadFilePath"],file_name)

    file_descriptor = os.open(formatted_file_path, os.O_CREAT | os.O_WRONLY)
    os.set_inheritable(1, True)

    return file_descriptor