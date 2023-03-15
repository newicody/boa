#!/usr/bin/env python3
import io
import sys
import socket
import select
import os
import threading
import json
import ssl

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
    def __init__(self,req,authorized_path):
        self.req = req
        self.state="connected"
        self.close=0
        self.path = authorized_path

        self.index = ["index.php","index.html"]

        self.listing = None

        self.ressources = "res"
        self.errors = "errors"


    def recept(self):
        self.msg = self.req.recv(1024).decode("utf-8")
        self.state="requested"
        print(self.msg)
        self.armor = self.msg.split('\r')[0].split(' ')
        self.type = self.armor[0] # GET ...
        self.option = self.armor[1] # /xx/xxx/xxx/x.xxx
        #print(self.type)

    def valid_path(self):
        if self.option =="/":
            self.filepath = self.path # (self.path = root)
            self.file=None
            self.fileext=None

        elif self.option[-1]=="/": #and len(self.option)>1:
            self.outpath = self.option[1::]
            self.filepath = self.path+self.option[1::]
            self.file=None
            self.fileext=None

        else:
            self.filepath = self.option.split("/")
            self.filepath.pop(0)
            self.file = self.filepath.pop(-1)

            if len(self.file.split('.'))>1: 
                self.fileext = self.file.split('.')[1]
            else:
                self.fileext = None

            self.filepath = '/'.join(self.filepath)
            self.filepath = self.path + ''.join(self.filepath)


        self.state = "path completed"

    def valid_file(self):
        if self.fileext != None:
            if len(self.fileext.split('php?'))>1:
                self.phparg=self.fileext.split('php?')[0].split("&")
                self.fileext="php"
            else:
                self.phparg=None
        self.state = "extension verified"

    def path_accesible(self):

        if os.path.exists(self.filepath) is False:
            print("erreur accessing pa0th")
            self.filepath = self.path + '/errors/'
            self.file="404.html"
            self.mime = "text/html"
            self.fileext="html"

        self.state="path access verified"

    def add_defaut_index(self):
        for elt in os.listdir(self.filepath):
            for elt2 in self.index:
                if elt == elt2:
                    self.file = elt
                    self.fileext = elt.split(".")[1]
                    self.listing = None
                    return

        self.listing = os.listdir(self.filepath)
        self.file = "listing.php"
        self.filepath = self.path + self.ressources
        
        self.fileext = "php"


    def file_accesible(self):
        try:
            with open(self.filepath+'/'+self.file): pass
        except IOError:
            print("le fichier nexiste pas ou vous n'avez pas la permission pour y acceder en lecture")
            self.filepath = self.path + '/errors/'
            self.file="404.html"
            self.mime = "text/html"
            self.fileext="html"
        self.state = "access verified"


    def mime_detect(self):
        self.php = False
        if (self.type == "GET"):
            if (self.fileext == "php"):
                self.mime = "text/html"
                self.php = True
            elif (self.fileext == "html"):
                self.mime = "text/html"
            elif (self.fileext == "txt"):
                self.mime = "text/html"
            elif (self.fileext == "js"):
                self.mime = "text/javascript"
            elif (self.fileext == "ico"):
                self.mime = "image/x-icon"
            elif (self.fileext == "bin"):
                self.mime = "application/octet-stream"
            elif (self.fileext == None):
                self.mime = "application/octet-stream"
            else:
                self.mime = "text/html"

        elif (self.type == "POST"):
            if (self.fileext == "php"):
                self.mime = "text/html"
                self.php = True
        self.state = "analyzed"

    def php_args(self):
        #self.getphparg = self.phparg
        self.postphparg = ""
        if self.listing == None and self.msg.split("\n")[-1] != "":
            self.postphparg = " dest " + self.filepath + self.file
            for elt,elt2 in json.loads(self.msg.split("\n")[-1]).items():
                self.postphparg +=  " " + elt + " " + elt2
        elif (self.listing == None):
            self.postphparg = " dest " + self.filepath +"/"+ self.file


        elif self.listing != None:
            self.postphparg = " dest " + self.filepath + "/" + self.file + " path " + self.outpath
            x=0
            for elt in self.listing:
                self.postphparg += " " + str(x) + " " + elt
                x+=1
            print(self.postphparg)

        self.state = "arguments readed"

    def mime_php(self):
        self.f1 = bytes(os.popen(rf"php " + self.path + "res/" + "wrapper.php " + self.postphparg ).read(),'utf-8')
        self.php = False
        self.state = "php accessed"

    def mime_text(self):
        self.f2 = open(self.filepath+'/'+self.file,"rb")
        self.f1 = self.f2.read()
        self.f2.close()
        self.state = "text accessed"

    def create_header(self):
        self.header = 'HTTP/1.1 200 OK\n'
        self.mimetype = self.mime
        self.header += 'Content-Type: '+ str(self.mimetype) + '\n'
        self.header += 'Content-Length: ' + str(len(self.f1)) + '\n\n'
        self.finhead = bytes(self.header,'utf-8')
        self.state = "header created"

    def create_final_io(self):
        self.send = io.BytesIO( self.finhead + self.f1 )
        self.state = "finalized"

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
                chield.append(socket_chield(elt,root.path))
                chield[-1].recept()
                chield[-1].valid_path()
                chield[-1].valid_file()
                chield[-1].path_accesible()
                if chield[-1].file == None:
                    chield[-1].add_defaut_index() #if not given: looking for
                chield[-1].file_accesible()
                chield[-1].mime_detect()
                if chield[-1].php == True:
                    chield[-1].php_args()
                    chield[-1].mime_php()
                else:
                    chield[-1].mime_text()
                chield[-1].create_header()
                chield[-1].create_final_io()
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
# https
# fakemysql auth
# state
# writing log a wait
# communicate with other servers
# git export ?
# path cloisonement
# test de charge
# add version
# progress managment & draw stats realtime
# benchmarking
# plugin rt developing websystem
# streaming :
# css
# list path
#python virtual env
#currents connections states...
#security understanding modules linux
# sysytem d
#open rc
# yaml mime type
# options d'éxecution :
# error file report


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

#todo
             print


             quit()
        try:
            arg = next(options)
        except StopIteration as e:
            arg = "socket_one.py"

    event = main()

