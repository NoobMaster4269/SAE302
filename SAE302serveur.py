#!/usr/bin/env python3
# Serveur TCP Multi Thread
import socket
import os
from _thread import *
import json
import sqlite3

ServerSocket = None
host = '127.0.0.1'
port = 7001
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
    con = sqlite3.connect('bdd2.db')
    cur = con.cursor()
    global nbclients
    print("Connection", connection)
    while True:
        data = connection.recv(2048)
        reply = data.decode('utf-8') + '\n'

        Nom = data.decode('utf-8')
        nom = json.loads(Nom) 
        Services = "\nChoisissez un des differents services : \n1. Creer une nouvelle promotion\n2. Ajouter un nouvel etudiant dans une promotion\n3. Ajouter une note (avec son coeficient) à un étudiant dans une promotion\n4. Demander le calcul de la moyenne d'un étudiant dans une promotion\n5. Demander le calcul de la moyenne d'une promotion\n6. Faire une liste d'etudiant et de leur note d'une promotion\n"

        #Ajoutée une promotion
        if nom["Services"] == "1":
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
            result = cur.fetchall()

            if len(result) > 0 and nom['Promotion'] == result[0][0]:
                connection.send(str.encode("\nLa promotion existe déjà."))
                connection.send(str.encode(Services))
           
            else:
                cur.execute(f"DROP TABLE IF EXISTS '{nom['Promotion']}';")
                con.commit()

                cur.execute(f"CREATE TABLE '{nom['Promotion']}' ('id{nom['Promotion']}' INTEGER PRIMARY KEY AUTOINCREMENT, NomPromo TEXT NOT NULL, Prenom TEXT NOT NULL, Nom TEXT NOT NULL);")
                con.commit()
                
                #CREATION DE LA TABLE NOTES 
                cur.execute(f"DROP TABLE IF EXISTS 'Notes{nom['Promotion']}';")
                con.commit()

                cur.execute(f"CREATE TABLE 'Notes{nom['Promotion']}' ('idNote{nom['Promotion']}' INTEGER PRIMARY KEY AUTOINCREMENT, 'id{nom['Promotion']}' INTEGER NOT NULL, NomPromo TEXT NOT NULL, Nom TEXT NOT NULL, Prenom TEXT NOT NULL, Note INTEGER NULL, Coef INTEGER NULL, FOREIGN KEY ('id{nom['Promotion']}') REFERENCES '{nom['Promotion']}' ('id{nom['Promotion']}'), FOREIGN KEY (NomPromo) REFERENCES '{nom['Promotion']}' (NomPromo), FOREIGN KEY (Nom) REFERENCES '{nom['Promotion']}' (Nom), FOREIGN KEY (Prenom) REFERENCES '{nom['Promotion']}' (Prenom)); ")
                con.commit()
          
                cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
                result2 = cur.fetchall()
                con.commit()


                if len(result2) > 0 and result2 == nom['Promotion']:
                    connection.send(str.encode("\nLa nouvelle promotion a bien été créée"))
                    connection.send(str.encode(Services))
                else:
                    connection.send(str.encode("\nLa promotion n'a pas été créée"))
                    connection.send(str.encode(Services))

        #Ajoute un Etudiant
        if nom["Services"] == "2":
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
            result = cur.fetchall()

            if len(result) > 0 and result[0][0] == nom['Promotion']:
                cur.execute(f"SELECT Prenom, Nom, NomPromo FROM '{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}' AND Prenom = '{nom['Prenom']}' AND Nom = '{nom['Nom']}'")
                result2 = cur.fetchall()
                if len(result2) > 0 and result2[0][0] == nom['Prenom'] and result2[0][1] == nom['Nom'] and result2[0][2] == nom['Promotion']:
                    connection.send(str.encode("\nL'etudiant existe déjà, change de prenom et de nom"))
                    connection.send(str.encode(Services))  
            
                else:
                    cur.execute(f"INSERT INTO '{nom['Promotion']}' (NomPromo, Prenom, Nom) VALUES ('{nom['Promotion']}', '{nom['Prenom']}', '{nom['Nom']}')")
                    con.commit()

                    connection.send(str.encode("\nEtudiant ajouter"))
                    connection.send(str.encode(Services)) 
            else:
                connection.send(str.encode("\nLa promotion n'existe pas"))
                connection.send(str.encode(Services))           
                

        #Ajouter une note
        if nom["Services"] == "3":
                cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
                result = cur.fetchall()

                if len(result) > 0 and result[0][0] == nom['Promotion']:
                        
                        cur.execute(f"SELECT Prenom, Nom FROM '{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}' AND Prenom = '{nom['Prenom']}' AND Nom = '{nom['Nom']}'")
                        result2 = cur.fetchall()

                        if len(result2) > 0 and result2[0][0] == nom['Prenom'] and result2[0][1] == nom['Nom']:
                            cur.execute(f"SELECT * FROM '{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}' AND Prenom = '{nom['Prenom']}' AND Nom = '{nom['Nom']}'")
                            result3 = cur.fetchall()
                    
                            cur.execute(f"INSERT INTO 'Notes{nom['Promotion']}' ('id{nom['Promotion']}', NomPromo, Nom, Prenom, Note, Coef) VALUES ('{result3[0][0]}', '{nom['Promotion']}', '{nom['Nom']}', '{nom['Prenom']}', '{nom['Note']}', '{nom['Coef']}')")
                            con.commit()
                            connection.send(str.encode(Services))
                        else:
                            connection.send(str.encode("\nL'etudiant n'existe pas"))
                            connection.send(str.encode(Services))                
                else:
                    connection.send(str.encode("\nLa promotion n'existe pas"))
                    connection.send(str.encode(Services))           
                

        #Calcul moyenne etudiant
        if nom["Services"] == "4":
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
            result = cur.fetchall()
            
            if len(result) > 0 and result[0][0] == nom['Promotion']:
                cur.execute(f"SELECT Prenom, Nom FROM '{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}' AND Prenom = '{nom['Prenom']}' AND Nom = '{nom['Nom']}'")
                result2 = cur.fetchall()

                if len(result2) > 0 and result2[0][0] == nom['Prenom'] and result2[0][1] == nom['Nom']:         
                    cur.execute(f"SELECT Note, Coef FROM 'Notes{nom['Promotion']}' WHERE Prenom = '{nom['Prenom']}' AND Nom = '{nom['Nom']}'")
                    result3 = cur.fetchall()
                    
                    if  len(result3) > 0 and result3[0][0] == nom['Note'] and result3[0][1] == nom['Coef']:
                        Num = 0 
                        Den = 0
                        for i in result2:
                            Num += i[0] * i[1]
                            Den += i[1]
                            moy = Num / Den

                        if moy < 8 :
                            connection.send(str.encode(f"La moyenne de {nom['Prenom']} est de {moy}, Nul go redoubler !"))
                            connection.send(str.encode(Services))

                        elif moy >= 8 and moy < 12: 
                            connection.send(str.encode(f"La moyenne de {nom['Prenom']} est de {moy}, Pas terrible comme la tara de tinou ! "))
                            connection.send(str.encode(Services))

                        elif moy >=12 and moy < 15:
                            connection.send(str.encode(f"La moyenne de {nom['Prenom']} est de {moy}, Très bien mais pas assez comparer au Goat NoobMaster."))
                            connection.send(str.encode(Services))

                        elif moy >=15:
                            connection.send(str.encode(f"La moyenne de {nom['Prenom']} est de {moy}, Exylos fait mieux.")) 
                            connection.send(str.encode(Services))
                    else:
                        connection.send(str.encode("\nL'etudiant n'a pas de note "))
                        connection.send(str.encode(Services))   
                else:
                    connection.send(str.encode("\nL'etudiant n'existe pas "))
                    connection.send(str.encode(Services))   
            else:
                connection.send(str.encode("\nLa promotion n'existe pas"))
                connection.send(str.encode(Services))           
                               

        #Calcul moyenne pormotion
        if nom["Services"] == "5":
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
            result = cur.fetchall()
            
            if len(result) > 0 and result[0][0] == nom['Promotion']:
                cur.execute(f"SELECT Note, Coef FROM 'Notes{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}'")
                result2 = cur.fetchall()
                
                if len(result2) > 0 and result2[0][0] == nom['Note'] and result2[0][1] == nom['Coef']:
                    Num = 0 
                    Den = 0
                    for i in  result2:
                        Num += i[0] * i[1]
                        Den += i[1]
                        moy = Num / Den

                    connection.send(str.encode(f"\nLa moyenne de la promotion {nom['Promotion']} est de {moy}")) 
                    connection.send(str.encode(Services))

                else:
                    connection.send(str.encode("\nLa promotion n'a pas de note "))
                    connection.send(str.encode(Services))
            else:
                connection.send(str.encode("\nLa promotion n'existe pas"))
                connection.send(str.encode(Services))           
                               
        #Liste etudiant et note d'une promotion
        if nom["Services"] == "6":
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{nom['Promotion']}'")
            result = cur.fetchall()
            
            if len(result) > 0 and result[0][0] == nom['Promotion']: 
                cur.execute(f"SELECT Prenom, Nom, Note, Coef FROM 'Notes{nom['Promotion']}' WHERE NomPromo = '{nom['Promotion']}'")
                result = cur.fetchall()

                for i in range (len(result)):
                    if liste:
                        liste = {"Prenom":result[i][0], "Nom":result[i][1], "Note":result[i][2], "Coef":result[i][3]}
                        lis = json.dumps(liste)
                    connection.send(str.encode(lis))
                
                connection.send(str.encode(Services))

            else:
                connection.send(str.encode("\nLa promotion n'existe pas"))
                connection.send(str.encode(Services))           
        
       # for client in clients:
        #    client.sendall(str.encode(reply))
        if data.decode('utf-8') == "quitter": # Bogue sur le quit !
            numclisent = int(connection.recv(2048))
            clients[numclient].close()
            clients.pop(numclient)
            nbclients-=1
        else:
            print(reply)

    con.close()     
        
if __name__== "__main__":
    main()