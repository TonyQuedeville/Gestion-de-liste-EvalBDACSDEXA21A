# -*- coding: utf-8 -*-
"""
23/01/2022
@author: Tony Quedeville
Studi.com
Bachelor développeur d'application Python.
Evaluation: BDACSDEXA21A (Gestion de liste)
"""


import datetime
from flask import Flask, jsonify, render_template, request
from Utilisateur import *
from Tache import *
#-----------------------------------------------------------------------------

class Index():
    # Initialisation ---------------------------------------------------------
    def __init__(self):  # Constructeur
        self.utilisateurJson = {
            'idUtilisateur': '',
            'nom': '',
            'prenom': '',
            'pseudo': '',
            'sex': '',
            'email': '',
            'motpass': '',
        }
        self.utilisateur = Utilisateur(self.utilisateurJson)
        self.tache = Tache()

        #webbrowser.open("http://localhost:5000/", 1)  # http://127.0.0.1:5000/
        self.createApp()
        # ------------------------------------------------------------------------

    # IHM app Web
    def createApp(self):
        app = Flask(__name__)
        
        # Page d'accueil (connexion)
        @app.route("/")
        def pageIndex():
            return render_template("index.html")
        #---"""

        # Identification Utilisateur
        @app.route("/identificationUtilisateurJson/")
        def readUtilisateur():
            self.utilisateur.pseudo = request.args.get('pseudo')

            reponse = self.utilisateur.identificationUtilisateur()
            if reponse == False:
                reponse = 0
            else:
                self.utilisateur.idUtilisateur = reponse[0][0]

            return jsonify(reponse)
        # ---"""

        # Se connecter
        @app.route("/connexion/")
        def connexion():
            self.utilisateur.pseudo = request.args.get('pseudo')
            self.utilisateur.motpass = request.args.get('motpass')

            if self.utilisateur.verifMotpass():
                reponse = self.utilisateur.readUtilisateur()
                if reponse == False:
                    reponse = -1
                else:
                    self.utilisateur.idUtilisateur = reponse
            else:
                reponse = 0

            return jsonify(reponse)
        # ---"""



        # Page tache
        @app.route("/taches/")
        def pageTache():
            return render_template("tache.html", pseudo=self.utilisateur.pseudo, idUtilisateur=self.utilisateur.idUtilisateur)
        # ---"""


        #---------------------------------------
        #CRUD

        # Créer une tâche
        @app.route("/initTachesJson/")
        def initTaches():
            self.tache.intituleTache = request.args.get('nomTache')
            self.tache.dateTache = request.args.get('dateTache')
            self.tache.statusTache = request.args.get('statusTache')
            self.tache.descripTache = request.args.get('descripTache')

            reponse = self.tache.initTache(request.args.get('idUtilisateur'))
            json = {'idTache': reponse}
            return jsonify(json)
        # ---"""

        # Lire une tâche
        @app.route("/readTachesJson/")
        def readTaches():
            if request.args.get('idTache') != None:
                self.tache.idTache = request.args.get('idTache')
            else:
                self.tache.idTache = ''

            if request.args.get('dateTache') != None:
                self.tache.dateTache = request.args.get('dateTache')
            else:
                self.tache.dateTache = ''

            if request.args.get('idUtilisateur') != None:
                idPseudoFiltre = request.args.get('idUtilisateur')
            else:
                idPseudoFiltre = ''

            reponse = self.tache.readTache(idPseudoFiltre)
            stat = calculStat(reponse)
            listeTaches = {"numTache":[], "tache":[], "pseudoUnique":[], "stat":[]}
            pseudoUniq = set() # set() élimine les doublons

            for i, tache in enumerate(reponse):
                listeTaches["numTache"].append(i)
                listeTaches["tache"].append(tache)
                pseudoUniq.add((tache[6],tache[7])) # set() élimine les doublons

            for ps in pseudoUniq: # Transfert le set dans la liste
                listeTaches["pseudoUnique"].append(ps)

            listeTaches["stat"].append(stat)

            return jsonify(listeTaches)
        # ---"""

        # Modifier une tache
        @app.route("/updateTachesJson/")
        def updateTaches():
            self.tache.idTache = request.args.get('idTache')
            self.tache.intituleTache = request.args.get('nomTache')
            self.tache.dateTache = request.args.get('dateTache')
            self.tache.statusTache = request.args.get('statusTache')
            self.tache.descripTache = request.args.get('descripTache')

            reponse = self.tache.updateTache()
            return jsonify(reponse)
        # ---"""

        # Supprimer une tâche
        @app.route("/deleteTachesJson/")
        def deleteTaches():
            self.tache.idTache = request.args.get('idTache')
            print(self.tache.idTache)
            # Action de suppression de la tache
            result = self.tache.deleteTache()
            return jsonify(result)
        # ---"""

        # Lancement de l'appli serveur
        app.run(
            debug=True
        )
        # ------------------------------------------------------------------------

def calculStat(reponse):
    # calcul et retourne le %age d'avancement des taches par status
    stat = []
    st = []

    for r in reponse:
        st.append(r[3])

    somme = st.count('à faire') + st.count('en cours') + st.count('terminée') + st.count('annulée')
    if somme > 0:
        stat.append((st.count('à faire')*100)//somme)
        stat.append((st.count('en cours')*100)//somme)
        stat.append((st.count('terminée')*100)//somme)
        stat.append((st.count('annulée')*100)//somme)
    else:
        stat = [0, 0, 0, 0]
    return stat

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":  # --- Programme de test ---
    Index()

