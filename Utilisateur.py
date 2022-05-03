# -*- coding: utf-8 -*-
"""
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)

Encodage Mot de passe : https://www.journaldufreenaute.fr/comment-chiffrer-un-mot-de-passe-en-python-a-laide-de-bcrypt/
"""
#-------------------------------------------------------------------------------------------------------------------
import sys
import mysql.connector as mysql
import bcrypt
#-------------------------------------------------------------------------------------------------------------------

class Utilisateur():
    def __init__(self, utilisateurJson):  # Constructeur
        self.idUtilisateur = utilisateurJson['idUtilisateur']
        self.pseudo = utilisateurJson['pseudo']
        self.motpass = utilisateurJson['motpass'].encode('utf-8')
        mp = "Studi"
        mp = mp.encode('utf-8')
        self.hacheMP = bcrypt.hashpw(mp,bcrypt.gensalt(10))

        # Connexion à la BDD
        try:
            self.connection = mysql.connect(
                user="root",
                password="BDACSDEXA21A",
                database='EvalBDACSDEXA21A',
                host='localhost'
            )
            self.cursor = self.connection.cursor()
            print("connexion BDD ok !")

        except mysql.connector.errors.InterfaceError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        # ---"""

    def verifMotpass(self):
        self.motpass = self.motpass.encode('utf-8')
        if bcrypt.checkpw(self.motpass, self.hacheMP):
            return True
        else :
            return False

    def readUtilisateur(self):
        """ Methode de lecture en BDD """
        requete = "SELECT * FROM utilisateur WHERE pseudo = '" + self.pseudo + "'"

        try:
            self.cursor.execute(requete)
            reponse = self.cursor.fetchall()
            print("read utilisateur BDD ok !")
            return reponse[0][0]
        except:
            self.connection.rollback()
            print("Erreur BDD ! : readTache()")
            return False
    #---"""

    def identificationUtilisateur(self):
        """ Methode de lecture en BDD """
        requete = "SELECT * FROM utilisateur WHERE pseudo = '" + self.pseudo + "'"

        try:
            self.cursor.execute(requete)
            reponse = self.cursor.fetchall()
            print("Identification utilisateur BDD ok !")
            return reponse
        except:
            self.connection.rollback()
            print("Erreur BDD ! : readTache()")
            return False
    #---"""
