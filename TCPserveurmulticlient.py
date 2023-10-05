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

        Nom = data.decode('utf-8')
        print(Nom)     
        nom = json.loads(Nom) 
        print(nom)

        #Ajouté une promotion
        if nom["Services"] == "1":
            cur.execute(f"INSERT INTO Promotion (NomPromo) VALUES ('{nom['NomPromo']}')")
            con.commit()

        #Ajoute un Etudiant
        if nom["Services"] == "2":
            cur.execute(f"INSERT INTO Etudiant (Prenom, Nom, NomPromo) VALUES ('{nom['Prenom']}','{nom['Nom']}'), '{nom['Promotion']}'")
            con.commit()
            #voir avec l'idPromo ?

        #Ajouter une note
        if nom["Services"] == "3":    
            cur.execute(f"SELECT idPromo FROM Promotion WHERE NomPromo = '{nom['Promotion']}'")
            result = cur.fetchall()
            con.commit()

            cur.execute(f"INSERT INTO Notes (idPromo, NomPromo, Nom, Prenom, Note, Coef) VALUES ('{result}', '{nom['Promotion']}', '{nom['Nom']}', '{nom['Prenom']}', '{nom['Note']}', '{nom['Coef']}' )")
            con.commit()
        
        #Calcul moyenne etudiant
        if nom["Services"] == "4":
            cur.execute(f"SELECT Note, Coef FROM Notes WHERE Prenom = '{nom["Prenom"]}'")
            result = cur.fetchall()
            con.commit()

        #a finir
            for i in range :
                Num =+ result['Note']*result['Coef']
                Den =+ result['Coef']
                moy = Num / Den

            if moy < 8 :
                connection.send(str.encode(f"La moyenne de '{nom["Prenom"]}' est de '{moy}', Nul go redoubler"))
            elif moy >= 8 and moy < 12: 
                connection.send(str.encode(f"La moyenne de '{nom["Prenom"]}' est de '{moy}', Pas terrible comme la tara de tinou"))

            elif moy >=12 and moy < 15:
                connection.send(str.encode(f"La moyenne de '{nom["Prenom"]}' est de '{moy}', Très bien mais pas assez comparer a  NoobMaster le goat"))
            elif moy >=15:
                connection.send(str.encode(f"La moyenne de '{nom["Prenom"]}' est de '{moy}', Exylos fait mieux !")) 

        #Calcul moyenne pormotion
        if nom["Services"] == "5":
            cur.execute(f"SELECT Note, Coef FROM Notes WHERE NomPromo = '{nom["Promotion"]}'")
            result = cur.fetchall()
            con.commit()

            #a finir 
            for i in range :
                Num =+ result['Note']*result['Coef']
                Den =+ result['Coef']
                moy = Num / Den
            connection.send(str.encode(f"La moyenne de la promotion '{nom["Promotion"]}' est de '{moy}'")) 
            

        

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