#!/usr/bin/env python3
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3000))
msg = input('')
client.sendall(msg)
client.close() 