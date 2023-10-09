#!/usr/bin/env python3
import socket
import _thread imoprt *
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msgServer = client.recv(1024).decode("utf-8")
print("Message du serveur : ", msgServer)
client.connect(("localhost", 3000))
msg = input('')
client.send(str.encode(msg))
client.sendall(msg)
client.close() 
