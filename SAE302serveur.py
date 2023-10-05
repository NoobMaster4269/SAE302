#!/usr/bin/env python3
import socket
import sqlite3
# initialisation du serveur


conn = sqlite3.connect('bdd.db')

cur = conn.cursor()


serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()


while True :
    client, infosclient = serveur.accept()
    request = client.recv(1024)
    serveur.sendall(b"i am the server",)
    print("Services dipobibles :\n")    
    if request.decode("utf-8") == "caca":
        print("Message client : ", request.decode("utf-8"))
        print("IP client connecté: ",socket.gethostbyname(socket.gethostname()))


    if request.decode("utf-8") == "2":
        insertsql = '''
    INSERT INTO rt1 (Nom, Prenom)
    VALUES (?, ?)
'''
        


    client.close()
serveur.close()