#!/usr/bin/env python3
import io
import sys
import socket
import select
import os
import threading

class new_socket:
    def __init__(self,port,path):
        self.hote = '192.168.1.158'
        self.port = port
        self.path = path
        self.connection = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.connection.bind((self.hote,self.port))
        self.connection.listen(10)

        print("Boa serving at port " + str(self.port) + " on " + self.path +" ( hote : " + self.hote + " )")

        self.waitingtoconnect=0
        self.connected=0
        self.toread=0
        self.downloading=0
        self.closing=0
        self.cpuload=0
        self.downspeed=0
        self.upspeed=0
        self.uptime=0
        self.precossclose=0

        self.timetowait = timetowait

        self.list_clients=[]
        self.state = "waiting for registering"

    def read_chield(self,timetowait):
        self.timetowait = timetowait
        self.clients_attentes, self.wlist, self.xlist = select.select([self.connection], [], [], self.timetowait)
        self.new_socket=len(self.clients_attentes)
        self.state="client entering"

    def connect(self):
        for client in self.clients_attentes:
            connect,infos = client.accept()
            self.list_clients.append(connect)
            self.state = "connected"

    def processing(self):
        self.valid=len(self.list_clients)-self.new_socket
        self.clienttoread,wlist,xlist = select.select(self.list_clients[self.valid:], [], [], 0.05)
        self.state = "listing"
    def recycle(self):
        return []
        self.state = "flushed"

class socket_chield:
    def __init__(self,req):
        self.req = req
        self.state="connected"
        self.close=0
    def recept(self):
        self.msg = self.req.recv(1024).decode("utf-8")
        self.state="requested"
        print(self.msg)
        self.armor = self.msg.split('\r')[0].split(' ')
        
    def mime_detect(self):
        self.php = False
        self.type = self.armor[0]
        self.option = self.armor[1]
        if (self.type == "GET") and (self.option[0]== "/" ) and (self.option != "/?" ):
            if (self.option == "/") or (self.option == "/index.html") or (self.option == "/index.php"):
                self.mime = "text/html"
                self.file="index.html"
            elif (self.option.split('?')[0].split('.')[1] == "php"):
                self.mime = "text/html"
                self.php = True
            elif (self.option.split(".")[1] == "html"):
                self.mime = "text/html"
                self.file=self.option[1:]
            elif (self.option.split(".")[1] == "js"):
                self.mime = "application/javascript"
                self.file=self.option[1:]
            elif (self.option.split(".")[1] == "ico"):
                self.mime = "image/x-icon"
                self.file=self.option[1:]
            elif (self.option.split('.')[-1] == "bin"):
                print(self.option)
                self.file=self.option[1:]
                self.mime = "application/octet-stream"
            else:
                self.file="404.html"
                self.mime = "text/html"

        try:
            with open(self.file): pass
        except IOError:
            print("le fichier nexiste pas")
            self.file="404.html"
            self.mime = "text/html"

        self.state="analyzed"

        self.header = 'HTTP/1.1 200 OK\n'
        self.mimetype = self.mime
        self.header += 'Content-Type: '+str(self.mimetype)+'\n\n'
        self.finhead = bytes(self.header,'utf-8')

    def mime_php(self):
        self.opt = self.option.split("?")[1].split("&")
        cmd = 'php-cgi -f ' + self.option.split("?")[0][1:] + " "
        for elt in self.opt:
            cmd += elt + " "
        self.f1 = os.popen(cmd).read()
        print(self.f1)
        self.send = io.BytesIO(self.finhead + bytes(self.f1,'utf-8'))
        self.php = False
        self.state="accessed"

    def mime_text(self):
        self.fl =open(self.file,"rb")
        self.send = io.BytesIO(self.finhead + self.fl.read())
        self.fl.close()
        self.state="accessed"

    def response(self):
        while f := self.send.read():
            self.req.send(f)
        self.state = "transfered"
        self.close = 1
#        root.list_clients[x] = "transfered"

def main():
    root = new_socket(port_value,path_value)
    chield = []
    send = []
    while True:
        root.read_chield(timetowait)
        root.connect()
        root.processing()
        if( root.clienttoread != []):
            for elt in root.clienttoread:
                chield.append(socket_chield(elt))
                chield[-1].recept()
                chield[-1].mime_detect()
                if chield[-1].php == True:
                    chield[-1].mime_php()
                else:
                    chield[-1].mime_text()
            #chield[-1].response()
                    send.append( threading.Thread(target=chield[-1].response))
                    send[-1].start()
        x=0
        for elt in send:
            if elt.is_alive() == False:
                root.list_clients[x].close()
            x+=1
            #root.clienttoread = []

  #      elif root.valid>0 :
  #          pass
                #
                #mysocket.list_clients = mysocket.recycle()
                #chield = socket_chield.recycle()



if __name__ == '__main__':

    port_value = 8081
    path_value = "./"

    timetowait = 0.05 # seconds:

    options = iter(sys.argv)
    arg = next(options)
    arg = next(options)

    while arg!="socket_one.py":
        if (arg == "-p") or (arg == "--port"):
             try:
                 port_value = int(next(options))
             except StopIteration as e:
                 print("Missing parameter after -p/--port")
        if (arg == "-r") or (arg == "--root"):
             try:
                 path_value = next(options)
             except StopIteration as e:
                 print("Missing parameter after -r/--root")
        if (arg == "-t") or (arg == "--timing"):
             try:
                 timetowait = next(options)
             except StopIteration as e:
                 print("Missing parameter after -t/--timing")
        if (arg == "-h") or (arg == "--help"):
             print("Utilisation : python3 socket_one.py [OPTION]")
             print("B.O.A est un serveur web écrit grâce à Python.\r")
             print("-r, --root         Change defaut path(./)\r")
             print("-p, --port         Change defaut port(8081)\r")
             print("-t, --timing       Change time to wait between each waiting connection(0.05)\r")
             print("-h, --help         Print this help\r")
             quit()
        try:
            arg = next(options)
        except StopIteration as e:
            arg = "socket_one.py"

    main()

