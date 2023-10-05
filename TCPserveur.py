#!/usr/bin/env python3
import socket
# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()
while True :
    client, infosclient = serveur.accept()
    request = client.recv(1024)
    if request.decode("utf-8") == "caca":
        print("Message client : ", request.decode("utf-8"))
        print("IP client connecté: ",socket.gethostbyname(socket.gethostname()))
       
    client.close()
serveur.close()