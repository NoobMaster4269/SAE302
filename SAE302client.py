#!/usr/bin/env python3
import socket
import os
from _thread import *
import json
ClientSocket = None
host = '127.0.0.1'
port = 7001
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
        print("\nChoisissez un des differents services :")
        print("1. Creer une nouvelle promotion\n2. Ajouter un nouvel etudiant dans une promotion\n3. Ajouter une note (avec son coeficient) à un étudiant dans une promotion\n4. Demander le calcul de la moyenne d'un étudiant dans une promotion\n5. Demander le calcul de la moyenne d'une promotion\n")
        start_new_thread(threaded_server, (ClientSocket, myNumber))
    while True:
        msg = input('') # bloquant les retours => nécessite un thread

        if msg == "1":
            print("Nom de la promotion :")
            msg2 = input('')
            nom = {"Services":msg, "Promotion": msg2}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "2":
            print("Prenom :")
            print("Nom : ")
            print("Nom de la promotion : ")
            msg1 = input('')
            msg2 = input('')
            msg3 = input('')
            nom = {"Services":msg, "Prenom":msg1,"Nom": msg2, "Promotion": msg3}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "3":
            print("Prenom de l'etudiant :")
            print("Nom de l'etudiant :")
            print("Promotion de l'etudiant :")
            print("Note de l'étudiant: ")
            print("Coefficiant de la note : ")
            msg1 = input('')
            msg2 = input('')
            msg3 = input('')
            msg4 = input('')
            msg5 = input('')
            nom = {"Services":msg, "Prenom":msg1, "Nom": msg2, "Promotion": msg3, "Note":msg4, "Coef":msg5}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "4":
            print("Prenom de l'etudiant :")
            print("Promotion de l'etudiant :")
            msg1 = input('')
            msg2 = input('')
            nom = {"Services":msg, "Prenom":msg1, "Promotion":msg2}
            Nom = json.dumps(nom)
            ClientSocket.send(Nom.encode())

        if msg == "6":
            print("Nom de la promotion : ")
            msg1 = input('')
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
