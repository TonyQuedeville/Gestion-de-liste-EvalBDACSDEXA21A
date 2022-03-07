# -*- coding: utf-8 -*-
"""
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)
"""

#-------------------------------------------------------------------------------------------------------------------
import sys
import mysql.connector as mysql
#-------------------------------------------------------------------------------------------------------------------

class Tache():
    # Constructeur
    def __init__(self, idTache = 0, intituleTache = '', dateTache = '', statusTache = 0, descripTache = '', idUtilisateur = 0):
        self.idTache = idTache
        self.intituleTache = intituleTache
        self.dateTache = dateTache
        self.statusTache = statusTache
        self.descripTache = descripTache
        self.idUtilisateur = idUtilisateur

        # Connexion à la BDD
        try:
            self.connection = mysql.connect(
                user="root",
                password="One2free!",
                database='EvalBDACSDEXA21A',
                host='localhost'
            )
            self.cursor = self.connection.cursor()
            print("connexion BDD ok !")

        except mysql.connector.errors.InterfaceError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        #---"""

    #---------------------------

    # Méthodes requètes BDD
    def initTache(self, idUtilisateur):
        """ Methode de création d'une tache en BDD """
        self.idUtilisateur = idUtilisateur

        requete = "INSERT INTO tache (intitule, date, status, descriptif, id_utilisateur) "
        requete = requete + "VALUES ('" + self.intituleTache + "', '" + self.dateTache + "', '" + self.statusTache + "', '" + self.descripTache + "', " + self.idUtilisateur + ")"

        try:
            self.cursor.execute(requete)
            self.connection.commit()

            try:
                self.cursor.execute("SELECT LAST_INSERT_ID()")
                reponse = self.cursor.fetchall()
                return reponse[0][0]
            except:
                self.connection.rollback()
                print("Erreur BDD ! : Last-insert-id()")
                return 0
        except:
            self.connection.rollback()
            print("Erreur BDD ! : createTache()")
            return 0
    #---"""

    def readTache(self, idUtilisateur):
        """ Methode de lecture d'une tache en BDD """
        closeWhere = False

        requete = "SELECT tache.*, utilisateur.id, utilisateur.pseudo FROM tache " \
                  "LEFT JOIN utilisateur ON id_utilisateur = utilisateur.id "
        if self.idTache or self.dateTache or idUtilisateur:
            if self.idTache:
                if closeWhere == True:
                    requete = requete + " AND "
                else:
                    requete = requete + "WHERE "
                    closeWhere = True
                requete = requete + "tache.id = '" + self.idTache + "'"

            if self.dateTache:
                if closeWhere == True:
                    requete = requete + " AND "
                else:
                    requete = requete + "WHERE "
                    closeWhere = True
                requete = requete + "tache.date = '" + self.dateTache + "'"

            if idUtilisateur:
                if closeWhere == True:
                    requete = requete + " AND "
                else:
                    requete = requete + "WHERE "
                    closeWhere = True
                requete = requete + "tache.id_utilisateur = '" + idUtilisateur + "'"
            #-"""

        print(requete)

        try:
            self.cursor.execute(requete)
            reponse = self.cursor.fetchall()
            #self.connection.commit() # pas de commit pour de requete de lecture (GET)
            print("read tache BDD ok !")
            return reponse
        except:
            self.connection.rollback()
            print("Erreur BDD ! : readTache()")
            return 0
    #---"""

    def updateTache(self):
        """ Methode de modification d'une tache en BDD """
        #requete = "UPDATE tache SET " + "intitule = '" + self.intituleTache + "',  date = '" + self.dateTache + "',  status = '" + self.statusTache + "',  descriptif = '" + self.descripTache + "' WHERE tache.id = " + self.idTache
        requete = "UPDATE tache SET "
        if self.intituleTache:
            requete = requete + "intitule = '" + self.intituleTache + "', "
        if self.dateTache:
            requete = requete + "date = '" + self.dateTache + "', "
        if self.descripTache:
            requete = requete + "descriptif = '" + self.descripTache + "', "
        #if idUtilisateur:
        #    requete = requete + "id_utilisateur = '" + idUtilisateur + "', "
        if self.statusTache:
            requete = requete + "status = '" + self.statusTache + "' "

        requete = requete + " WHERE tache.id = " + self.idTache
        print(requete)

        try:
            self.cursor.execute(requete)
            self.connection.commit() # commit pour une requete d'ecriture (POST)
            print("update tache BDD ok !")
            return 1
        except:
            self.connection.rollback()
            print("Erreur BDD ! : updateTache()")
            return 0
    #---"""

    def deleteTache(self):
        """ Methode de suppression d'une tache en BDD """
        requete = 'DELETE FROM tache WHERE id = ' + self.idTache
        print(requete)

        try:
            self.cursor.execute(requete)
            self.connection.commit() # commit pour une requete d'ecriture (POST)
            return 1
        except:
            self.connection.rollback()
            print("Erreur BDD ! : deleteTache()")
            return 0
    #---"""





    # Méthodes complèmentaires à n'utiliser que si besoin
    # Les tables tache, utilisateur et liste sont déjà créée avec MySQL Workbench
    def createTableTache(self):
        """ Methode de création de la table taches en BDD """
        try:
            requete = """
                        CREATE TABLE `EvalBDACSDEXA21A`.`tache` (
                          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                          `intitule` VARCHAR(45) NULL COMMENT 'intitulé: nom de la tache',
                          `date` DATETIME NULL COMMENT 'Date de la tache',
                          `status` VARCHAR(45) NULL COMMENT '0: NULL\n1: à faire\n2: en cours\n3: terminée\n4: annulée\'',
                          `descriptif` VARCHAR(500) NULL COMMENT 'descriptif de la tache (200 caractères max)',
                          `id_utilisateur` INT NULL COMMENT 'Identifiant de l’initiateur de la tache',
                          PRIMARY KEY (`id`),
                          UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);
                       """
            self.cursor.execute(requete)
            self.connection.commit()
            print("create Table tache BDD ok !")
            return True
        except:
            self.connection.rollback()
            print("Erreur BDD ! : createTableTache()")
            return False
    #---"""

    def createTableUtilisateur(self):
        """ Methode de création de la table utilisateur en BDD """
        try:
            requete = """
                        CREATE TABLE `EvalBDACSDEXA21A`.`utilisateur` (
                          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                          `nom` VARCHAR(45) NULL,
                          `prenom` VARCHAR(45) NULL,
                          `pseudo` VARCHAR(45) NULL,
                          `sex` INT UNSIGNED NULL COMMENT '0: Homme\n1: Femme',
                          `email` VARCHAR(45) NULL COMMENT 'Adresse mail utilisateur',
                          UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
                          PRIMARY KEY (`id`));
                       """
            self.cursor.execute(requete)
            self.connection.commit()
            print("create Table utilisateur BDD ok !")
            return True
        except:
            self.connection.rollback()
            print("Erreur BDD ! : createTableUtilisateur()")
            return False
    #---"""

    def createTableListe(self):
        """ Methode de création de la table liste en BDD """
        try:
            requete = """
                        CREATE TABLE `Studi`.`listeTache` (
                       """
            self.cursor.execute(requete)
            self.connection.commit()
            print("create Table liste BDD ok !")
            return True
        except:
            self.connection.rollback()
            print("Erreur BDD ! : createTableListe()")
            return False
    #---"""


#--------------------------------------------------------------------------------------------------------------