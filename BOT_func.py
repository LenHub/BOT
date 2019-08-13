import os
import pickle
import datetime as dt
from random import randrange
from math import ceil

def recup_scores():
    """Cette fonction récupère les scores enregistrés si le fichier existe.
    Dans tous les cas, on renvoie un dictionnaire,
    soit l'objet dépicklé,
    soit un dictionnaire vide.
    On s'appuie sur nom_fichier_scores défini dans donnees.py"""

    if os.path.exists("scores"):  # Le fichier existe
        # On le récupère
        fichier_scores = open("scores", "rb")
        mon_depickler = pickle.Unpickler(fichier_scores)
        scores = mon_depickler.load()
        fichier_scores.close()
    else:  # Le fichier n'existe pas
        scores = {}
    return scores

def enregistrer_scores(scores):
    """Cette fonction se charge d'enregistrer les scores dans le fichier
    nom_fichier_scores. Elle reçoit en paramètre le dictionnaire des scores
    à enregistrer"""

    fichier_scores = open("scores", "wb") # On écrase les anciens scores
    mon_pickler = pickle.Pickler(fichier_scores)
    mon_pickler.dump(scores)
    fichier_scores.close()

def log(id,msg):
    date = str(dt.datetime.now())
    date = date.split('.')[0]
    message = date + ' : ' + id + ' ' + msg +'\n'
    print(id + ' > ' + message)
    with open('log.txt','a', encoding='utf-8') as f:
        f.write(message)

"""
def defi(nom,code,reponse,indice,msg):
    if msg.find('-r') != -1:
        rep = msg.split(' ')[2]
        if rep == reponse:
            val = data[id].def2
            data[id].val(nom)
            if val:
                irc.private(id, 'Tu as déjà validé ce défi')
                log(id, nom + ' déjà validé ' + msg)
            else:
                irc.private(id, 'Bien joué, tu as gagné 5 points')
                log(id, nom +' validé ' + msg)
            enregistrer_scores(data)
        else:
            data[id].punish(1)
            irc.private(id, 'Raté, tu as perdu un point')
            enregistrer_scores(data)
            log(id, 'def2 erreur ' + msg)
    else:
        irc.send('Pour valider le défi, il te faut déchiffrer le mot de passe caché dans la phrase suivante:')
        time.sleep(0.5)
        irc.send(code)
        time.sleep(0.5)
        irc.send('Indice: '+ indice+'. Envoie ta réponse par message privé sous la forme suivante : !def2 -r réponse')
        log(id, msg)
"""

class Joueur:
    def __init__(self,id):
        self.id = id
        self.score = 0
        self.def1 = False
        self.def2 = False
        self.def3 = False
        self.def4 = False
        self.def5 = False
        self.def6 = False
        self.def7 = False
        self.def8 = False
        self.def9 = False
        self.def10 = False
        self.def11 = False
        self.def12= False
        self.def13= False
        self.def14= False
        self.def15= False
        self.def16 = False
        self.def17 = False
        self.def18 = False
        self.def19 = False
        self.def20 = False
        self.def21 = False
        self.def22 = False
        self.def23 = False
        self.def24 = False
        self.def25 = False
        self.def26 = False
        self.def27 = False
        self.def28 = False
        self.def29 = False
        self.def30 = False


    def val(self, defi):
        if defi == 'def1' and self.def1 == False:
            self.score += 5
            self.def1 = True

        elif defi == 'def2' and self.def2 == False:
            self.score += 5
            self.def2 = True

        elif defi == 'def3' and self.def3 == False:
            self.score += 10
            self.def3 = True

        elif defi == 'def4' and self.def4 == False:
            self.score += 5
            self.def3 = True

    def setscore(self, pts):
        self.score = pts

    def punish(self,pts):
        self.score -= 1

    def add(self,pts):
        self.score += pts



