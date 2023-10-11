#!/usr/bin/env python3
import socket
import os
from _thread import *
import json

ClientSocket = None
host = '127.0.0.1'
port = 4500
myNumber = 0

def main():
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    finally:
        print("Connecter au Serveur !")
        myNumber = int(ClientSocket.recv(1024))
        #print("myNumber client received : ", myNumber, "\n")
        print("\nChoisissez un des differents services : \n1. Creer une nouvelle promotion\n2. Ajouter un nouvel etudiant dans une promotion\n3. Ajouter une note (avec son coeficient) à un étudiant dans une promotion\n4. Demander le calcul de la moyenne d'un étudiant dans une promotion\n5. Demander le calcul de la moyenne d'une promotion\n6. Faire une liste d'etudiant et de leur note d'une promotion\n")
        start_new_thread(threaded_server, (ClientSocket, myNumber))
    while True:
        msg = input('') # bloquant les retours => nécessite un thread

        if msg == "1":
            msg2 = input('Nom de la promotion : ')
            nom = {"Services":msg, "Promotion": msg2}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "2":
            msg1 = input('Prenom : ')
            msg2 = input('Nom : ')
            msg3 = input('Nom de la promotion : ')
            nom = {"Services":msg, "Prenom":msg1,"Nom": msg2, "Promotion": msg3}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "3":
            msg1 = input('Prenom de l\'etudiant : ')
            msg2 = input('Nom de l\'etudiant : ')
            msg3 = input('Promotion de l\'etudiant : ')
            msg4 = input('Note de l\'étudiant: ')
            msg5 = input('Coefficiant de la note : ')
            nom = {"Services":msg, "Prenom":msg1, "Nom": msg2, "Promotion": msg3, "Note":msg4, "Coef":msg5}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "4":
            msg1 = input('Prenom de l\'etudiant : ')
            msg2 = input('Nom de l\'etudiant : ')
            msg3 = input('Promotion de l\'etudiant :')
            nom = {"Services":msg, "Prenom":msg1, "Nom":msg2, "Promotion":msg3}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "5":
            msg1 = input('Nom de la promotion : ')
            nom = {"Services":msg, "Promotion":msg1}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

 
            #ClientSocket.send(str.encode(msg))

        if msg == "quitter": # Bogue sur le quit !
            ClientSocket.send(str.encode(str(myNumber)))
            break


def threaded_server(connection, num):
    while True:
        response = connection.recv(1024)
        print(response.decode('utf-8'))

if __name__== "__main__":
    main()
