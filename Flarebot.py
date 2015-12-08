import random
import socket
import time
#import socks
server = "irc.freenode.net" # Server
channel = "#sctfio" # Channel

#server = "irc.easyctf.com" # Server
#channel = "#easyctf" # Channel
botnick = "Flareboto" # Your bots nick

def ping(): # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :Pong\n")
  
def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
    ircsock.send("JOIN "+ chan +"\n")

def hello(newnick):
    ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

class NoVocab:
    def __init__(self):
        self.insults = ['fat','gay','a geyfat','retarded']
        self.compliments = ['the greatest']
        self.wants = ['flag','food','results']
    def reply(self, name=None):
        resp = ["you're",'your mom is','because']
        if name:
            resp += [name + ' is']
        choice = random.randint(1,5)
        if choice == 1:
            out = random.choice(resp)+' '+random.choice(self.insults)
        elif choice == 2:
            out = "i'm "+random.choice(self.compliments)
        elif choice == 3:
            out = 'give me '+random.choice(self.wants)
        elif choice == 4:
            out = 'no'
        elif choice == 5:
            out = 'that\'s g'+random.randint(1,3)*'oo'+'d'
        else:
            out = 'krusty'
    
        nr = random.random()
        if nr > .4:
            out = out.replace('give','gib')
        nr = random.random()
        if nr > .4:
            out = out.replace('eat','8')
            out = out.replace('ate','8')
        nr = random.random()
        if nr > .4:
            out = out.replace("you're",'ur').replace('your','ur')
        nr = random.random()
        if nr > .5:
            out = out.replace("flag",'fleg')

        nr = random.random()
        if nr > .5:
            out = out.replace("that's",'daz')
            out = out.replace('oo','uu')

        nr = random.random()
        if nr > .5:
            out = out.replace("because",'coz')
        return out

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
#ircsock = socks.socksocket()
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :MGQ_Man\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined
a = NoVocab()
lastmsg = time.time()
time.sleep(1)
while 1:
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server
    if "this nickname is registered" in ircmsg.lower():
        sendmsg(channel, '/msg NickServ IDENTIFY xxxxxxxx')
    if "you have not registered" in ircmsg.lower():
        sendmsg(channel, '/msg NickServ IDENTIFY xxxxxxxx')
    if "nickname is already in use" in ircmsg.lower():
        sendmsg(channel, '/msg NickServ GHOST Flarebot xxxxxxx')
    if ircmsg.find("PING :") != -1:
        ping()
    
    if ircmsg.lower().find('mgq') != -1:
        sendmsg(channel, 'magical gay quest?')
    elif ircmsg.lower().find('fuck') != -1 or ircmsg.lower().find('shit') != -1:
        sendmsg(channel, 'LANGUAGE!')
    
        
    elif ircmsg.lower().find(botnick.lower()) != -1:
        user = ircmsg.split(':')[1].split('!')[0]
        rep = a.reply(random.choice([user,user+'shar']))
        sendmsg(channel, rep)
    elif ircmsg.lower().find('flarebot') != -1:
        user = ircmsg.split(':')[1].split('!')[0]
        rep = a.reply(random.choice([user,user+'shar']))
        sendmsg(channel, rep)
    elif len(ircmsg)>5 and 'PING' not in ircmsg[:6]:
        if random.random()>.8:
            rep = a.reply()
            sendmsg(channel, rep)
        lastmsg = time.time()
    elif abs(time.time() - lastmsg) > 80:
        rep = a.reply()
        sendmsg(channel, rep)
