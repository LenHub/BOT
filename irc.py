import socket
import time

class IRC:
    """Créé par Len, permet la communication avec un serveur IRC"""
    irc = socket.socket()

    def __init__(self,salon):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chan = salon

    def send(self, msg):
        self.irc.send(bytes("PRIVMSG " + self.chan + " : " + msg + "\r\n",'utf-8'))

    def private(self,id,msg):
        self.irc.send(bytes("PRIVMSG " + id + " : " + msg + "\r\n", 'utf-8'))


    def connect(self, server, botnick):
        # defines the socket
        print("Connnexion à :" + server)
        self.irc.connect((server, 6667))  # connects to the server
        time.sleep(1)
        print('> Chargement du salon ...')
        self.irc.send(bytes(
            "USER " + botnick + " " + botnick + " " + botnick + " :Bot de challenge\r\n",'utf-8'))
        time.sleep(1)
        self.irc.send(bytes("NICK " + botnick + "\r\n", 'utf-8'))
        time.sleep(1)
        self.irc.send(bytes("JOIN " + self.chan + "\r\n", 'utf-8'))

        message = ''
        time.sleep(1)

        while message.find("End of /NAMES list.") == -1:
            # attend la fin du message d'accueil
            message = self.irc.recv(2048).decode("UTF-8")
            message = message.strip('\n\r')

        print('> En attente de messages ...')


    def recv(self):
        text = self.irc.recv(2048).decode('UTF-8')  # receive the text
        return text

    def recevoir(self):
        text = self.irc.recv(2048).decode('UTF-8')
        text = text.split(' :')
        text = text[-1]
        text = text.strip('\r\n')
        return text

    def close(self):
        self.irc.close()

    def ping(self):
        self.irc.send(b'PONG PING\r\n')
