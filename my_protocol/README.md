# My Protocol
This code has both a server and a client executeable. the server accepts incoming connections and the client sends the server messages.
Important concepts:
After the message is formulated an end of file indicator and the packet size is appended to the end of the message. 
By appending this to the end of the message and allowing our server to parse this. 
* We create a checksum that the server is able to see how many bytes were supposed to be received compared to what was received
* We are able to tell our server that it has received all files and to output the receieved input to the screen

## Project 
Your task: develop and implement a protocol to frame byte-array messages in a manner that they will arrive intact even if they are fragmented during transmission.  


## Getting started 
## Built with
[Python 3.7.3](https://www.python.org/downloads/release/python-373/)

## Prerequisites
### Python Version 3.7.3
    sudo apt-get update
    sudo apt-get install python3.7.3
### Python yaml package
    sudo apt-get install python-yaml
    sudo yum install python-yaml

## Configuration
Under the configs folder is the config.yaml file with configuration settings. These are the default values but can be updated as needed or as requirements change. 


## Examples of use 
**Notes**
* In the repo there are test files under the data directory that you can use and or modify or it will prompt you for input(see below).  
* You can also use a custom txt file containing passwords that are common or want to be exempted. Included in this package under the data folder is a common_passwords.txt that will be used by default if there isn't a txt file specifed.
### Without providing a file 

navigate to the my_protocol directory in the repo and run the following commands in seperate terminal windows

```sh
python3 server.py
```

```sh
python3 client.py
```

This will run the main executable file and prompt you to enter input into the command line to interpret. Pressing enter in this prompt will tell the module that you are done entering input and to process what has been entered so far

### With providing a file
```sh
python3 client.py < ./data/1023bytes.txt
```

This will run the main executable file and take in a file to FD0

## References 
* [Using os.read to read n bytes](https://www.geeksforgeeks.org/python-os-read-method/#:~:text=read()%20method%20in%20Python,bytes%20left%20to%20be%20read)
* [Interview Project](https://github.com/johnmdelgado/SRE-Project)
* [Project1](https://github.com/utep-cs-systems-courses/os-shell-johnmdelgado)

## License  
Distributed under the MIT License. See `LICENSE` for more information.
