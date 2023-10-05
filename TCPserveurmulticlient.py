#!/usr/bin/env python3
# Serveur TCP Multi Thread
import socket
import os
from _thread import *
import json
import sqlite3
ServerSocket = None
host = '127.0.0.1'
port = 6900
clients = []
nbclients = 0
numclient = None


def main():
    global nbclients
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    finally:
        print('Attente d\'une connexion...')
        ServerSocket.listen(5)
    while True:
        client, address = ServerSocket.accept()
        print('Connecter à : ' + address[0] + ':' + str(address[1]))
        client.send(str.encode(str(nbclients)))
        clients.append(client)
        print("Liste des clients : ", clients)
        start_new_thread(threaded_client, (client, ))
        nbclients+=1
        print('Nombre Thread : ' + str(nbclients))

def threaded_client(connection):
    con = sqlite3.connect('bdd.db')
    cur = con.cursor()
    global nbclients
    print("Connection", connection)
    while True:
        data = connection.recv(2048)
        reply = '\n>>' + data.decode('utf-8') + '\n'

        no = data.decode('utf-8')
        print(no)     
        nom = json.loads(no) 
        print(nom)

        if nom["Nomc"] == "1":
            cur.execute(f"INSERT INTO Promotion (NomPromo) VALUES ('{nom['NomPromo']}')")
            con.commit()

        
        
        if nom["Nomc"] == "2":
            cur.execute(f"INSERT INTO Etudiant (NomEtudiant) VALUES ('{nom['NomEtudiant']}'), '{nom['Promotion']}'")
            con.commit()



       # for client in clients:
        #    client.sendall(str.encode(reply))
        if data == "quit": # Bogue sur le quit !
            numclient = int(connection.recv(2048))
            clients[numclient].close()
            clients.pop(numclient)
            nbclients-=1
        else:
            print(reply)
    con.close()     
        
if __name__== "__main__":
    main()