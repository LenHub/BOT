from BOT_func import *
from irc import *
import time
"""
Programme créé par Lénaïc GAGER
"""

############################################################

hote = 'chat.freenode.net'
port = 6667
chan = '#Chat_de_Len'
botnick = 'Bot_de_Len'
admin = 'Len___'

############################################################

data = recup_scores()

irc = IRC(chan)
irc.connect(hote,botnick)
log('BOT','en ligne')

while True:
    rawmess = irc.recv()
    id = rawmess.split('!')[0]
    id = id.lstrip(':')

    if id not in data.keys() and id.find('PING') == -1:
        data[id] = Joueur(id)
        log('Nouveau joueur :',id)

    messages = rawmess.split(' :')
    message = messages[-1]
    message = message.strip('\r\n')
    if rawmess.find('PING') != -1:
        irc.ping()
        message = ''

    if len(message) != 0:
        if message.find('!') != -1:

            if message.find('!score') != -1:
                score = 'Score de ' + id + ' : ' + str(data[id].score)
                irc.send(score)
                log(id,'!score')

            elif message.find('!stop') != -1:
                if id == admin:
                    irc.close()
                    log(id,'!stop')
                    break
                else:
                    log(id,'COMMANDE INTERDITE: !stop')

            elif message.find('!setscore') != -1:
                if id == admin:
                    # message de la forme : !setscore/id/pts
                    set = message.split('/')
                    data[set[1]].setscore(int(set[2]))
                    enregistrer_scores(data)
                    log(id, message)
                else:
                    log(id,'COMMANDE INTERDITE: '+message)

            elif message.find('!add') != -1:
                if id == admin:
                    #message de la forme !add/id/pts
                    add = message.split('/')
                    data[add[1]].add(int(add[2]))
                    enregistrer_scores(data)
                    log(id,message)
                else:
                    log(id,'COMMANDE INTERDITE: '+ message)

            elif message.find('!roulette') != -1 and id == admin:
                irc.private(id,"Bienvenue à la roulette du ZCasino")

                solde = data[id].score
                continuer = True

                while continuer == True:
                    irc.private(id,"\nVous disposez de {0} €".format(solde))
                    mise = 0
                    EN_LIGNE = 0
                    while int(mise) <= 0 or int(mise) > int(solde):
                        irc.private(id,"Combien voulez vous miser ? :")
                        time.sleep(3)
                        mise = irc.recevoir()
                        while not mise.isdigit():
                            irc.private(id,"erreur")
                            irc.private(id,"Combien voulez vous miser ? :")
                            time.sleep(3)
                            mise = irc.recevoir()
                        if int(mise) <= 0:
                            irc.private(id,"Vous devez misez quelque chose\n")
                        elif int(mise) > int(solde):
                            irc.private(id,"Vous n'avez pas assez\n")
                        EN_LIGNE += 1
                        if EN_LIGNE == 3:
                            break

                    if EN_LIGNE == 3:
                        break
                    else:
                        EN_LIGNE = 0

                    solde -= float(mise)

                    print("\nChoississez une case entre 0 et 49")
                    pari = -1
                    while int(pari) < 0 or int(pari) > 49:
                        irc.private(id,"Sur quel numéro souhaitez vous déposer votre mise ? :")
                        time.sleep(3)
                        pari = irc.recevoir()
                        if int(pari) < 0 or int(pari) > 49:
                            irc.private(id,"Choisissez une case entre 0 et 49")
                    print("Vous avez misé {0}€ sur la case n°{1}".format(mise, pari))

                    print("\nLe croupier lance la bille")
                    bille = randrange(50)
                    print("La bille est tombée sur le numéro {0}".format(bille))

                    if pari == bille:
                        solde += ceil(float(mise) * 3) + float(mise)
                        print("Vous avez le bon numéro !")
                        print("Vous avez maintenant {0}€".format(solde))
                    elif int(bille) % 2 == int(pari) % 2:
                        solde += float(mise) + (float(mise)) / 2
                        print("La bille est tombée sur la même couleur que votre numéro")
                        print("Vous avez maintenant {0}€".format(solde))
                    else:
                        print("Pas de chance !")
                        print("Il vous reste {0}€".format(solde))

                    if solde <= 0:
                        print("\nVous n'avez plus d'argent")
                        continuer = False
                    elif solde > 0:
                        question = input("\nVoulez vous continuer ? (o/n) :")
                        if question.lower() == "oui" or question.lower() == "o":
                            continuer = True
                        elif question.lower() == "non" or question.lower() == "n":
                            continuer = False
                        else:
                            continuer = True


            elif message.find('!def1') != -1:
                if message.find('-r') != -1:
                    rep = message.split(' ')[2]
                    if rep == 'SECRET':
                        val = data[id].def1
                        data[id].val('def1')
                        if val:
                            irc.private(id, 'Tu as déjà validé ce défi')
                            log(id,'def1 déjà validé '+ message)
                        else:
                            irc.private(id, 'Bien joué, tu as gagné 5 points')
                            log(id, 'def1 validé ' + message)
                        enregistrer_scores(data)
                    else:
                        data[id].punish(1)
                        irc.private(id,'Raté, tu as perdu un point')
                        enregistrer_scores(data)
                        log(id,'def1 erreur '+ message)

                else:
                    irc.send('[5 pts] Pour valider le défi, il te faut déchiffrer le mot de passe caché dans la phrase suivante:')
                    time.sleep(0.5)
                    irc.send('Kdlnscdozrrddrsrdbqds')
                    time.sleep(0.5)
                    irc.send('Envoie ta réponse par message privé sous la forme suivante : !def1 -r réponse')
                    log(id,message)

            elif message.find('!def2') != -1:
                if message.find('-r') != -1:
                    rep = message.split(' ')[2]
                    if rep == 'coucou':
                        val = data[id].def2
                        data[id].val('def2')
                        if val:
                            irc.private(id, 'Tu as déjà validé ce défi')
                            log(id, 'def2 déjà validé ' + message)
                        else:
                            irc.private(id, 'Bien joué, tu as gagné 5 points')
                            log(id, 'def2 validé ' + message)
                        enregistrer_scores(data)
                    else:
                        data[id].punish(1)
                        irc.private(id, 'Raté, tu as perdu un point')
                        enregistrer_scores(data)
                        log(id,'def2 erreur '+message)

                else:
                    irc.send('[5 pts] Pour valider le défi, il te faut déchiffrer le mot de passe caché dans la phrase suivante:')
                    time.sleep(0.5)
                    irc.send('Y291Y291')
                    time.sleep(0.5)
                    irc.send('Indice: base 64. Envoie ta réponse par message privé sous la forme suivante : !def2 -r réponse')
                    log(id,message)

            elif message.find('!def3') != -1:
                if message.find('-r') != -1:
                    rep = message.split(' ')[2]
                    if rep.upper() == 'MDP':
                        val = data[id].def3
                        data[id].val('def3')
                        if val:
                            irc.private(id, 'Tu as déjà validé ce défi')
                            log(id, 'def3 déjà validé ' + message)
                        else:
                            irc.private(id, 'Bien joué, tu as gagné 5 points')
                            log(id, 'def3 validé ' + message)
                        enregistrer_scores(data)
                    else:
                        data[id].punish(1)
                        irc.private(id, 'Raté, tu as perdu un point')
                        enregistrer_scores(data)
                        log(id,'def3 erreur'+message)

                else:
                    irc.send('[10 pts] Pour valider le défi, il te faut déchiffrer le mot de passe suivant avec la clé 0010 :')
                    time.sleep(0.5)
                    irc.send('OFR')
                    time.sleep(0.5)
                    irc.send('Indice: Convertis le message crypté en binaire. Envoie ta réponse par message privé sous la forme suivante : !def3 -r réponse')
                    log(id,message)

            elif message.find('!def4') != -1:
                if message.find('-r') != -1:
                    rep = message.split(' ')[2]
                    if rep.lower() == 'motdepasse':
                        val = data[id].def4
                        data[id].val('def4')
                        if val:
                            irc.private(id, 'Tu as déjà validé ce défi')
                            log(id, 'def4 déjà validé ' + message)
                        else:
                            irc.private(id, 'Bien joué, tu as gagné 5 points')
                            log(id, 'def4 validé ' + message)
                        enregistrer_scores(data)
                    else:
                        data[id].punish(1)
                        irc.private(id, 'Raté, tu as perdu un point')
                        enregistrer_scores(data)
                        log(id,'def4 erreur'+message)

                else:
                    irc.send('[5 pts ]Pour valider le défi, il te faut déchiffrer le mot de passe suivant :')
                    time.sleep(0.5)
                    irc.send('B6EDD10559B20CB0A3DDAEB15E5267CC')
                    time.sleep(0.5)
                    irc.send('Indice: hash . Envoie ta réponse par message privé sous la forme suivante : !def4 -r réponse')
                    log(id,message)

        elif message.find('JOIN') != -1:
            print(id,'a rejoint le channel')
            log(id,'a rejoint le channel')

        else:
            # print(rawmess)
            print(id, '>', message)

    time.sleep(1)

enregistrer_scores(data)
log('BOT','hors ligne')
