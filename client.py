#!/usr/bin/python           # This is client.py file

import socket
import os              # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
ans = s.recv(1024)
command = "python "
final_command  = command + ans
print final_command
os.system(final_command)

s.close                     # Close the socket when done