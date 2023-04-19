import multiprocessing

from new_socket.new_socket import *
from socket_chield.socket_chield import *
import threading
import asyncio

import pickle

class poool:
    def __init__(self,manager):
        self.messages_pool  = manager.Queue()
        self.problems = manager.list()
    def mainprocess(self):
        while True:
            new_value = self.messages_pool.get()
            self.problems.append(new_value)

    def localpool_srv(self,port_value,timetowait,interface,ip,myerrors,mylog,mypool,ssll=False,ssl_file=False):
        self.port_value = int(port_value)
        self.timetowait = timetowait
        self.interface = interface
        self.ip = ip
        self.ssll = ssll
        self.ssl_file = ssl_file
        self.path_value=False


        self.messages_err = myerrors.messages_err
        self.messages_log = mylog.messages_log
        self.messages_pool = mypool.messages_pool

        root = new_socket(self.port_value,self.path_value,self.timetowait,self.interface,self.ip,self.ssll,self.ssl_file)
        chield = []
        send = []
        while True:
            root.read_chield(self.timetowait)
            root.connect()
            root.processing()
            if( root.clienttoread != []):
                print("new client on localpool")
                for elt in root.clienttoread:
                    chield.append(socket_chield(elt,myerrors,mylog,mypool,root.path))
                    chield[-1].recept2()
                    send.append(threading.Thread(target=chield[-1].response2))
                    send[-1].start()
                    #self.messages_log.put("connection")
            x=0
            for elt in send:
                if elt.is_alive() == False:
                    root.list_clients[x].close()
                x+=1

#    def localpool_clt(self,peer,connection,probleme,dest,head,filepath,pos):
    def localpool_clt(self,lstarg,peers): #  peer,req,file,head,pos
        a = lstarg[1].getpeername()
        b = lstarg[1].getsockname()
        for elt in peers:
            try:
                connectio = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                print("connection from " + b[0] + ":" + str(b[1]) + " to " + a[0] + ":" + str(a[1]))
                print("becoming from " + elt[0] + ":" + str(elt[1]) + " to " + a[0] + ":" + str(a[1]))
                print("connecting")
                connectio.connect((elt[0],int(elt[1])))
                print("send parameters")
                connectio.send(pickle.dumps([a,b,lstarg[2],lstarg[3],lstarg[4]]))
                break
            except:
                 continue
        #f = open(file,"rb")
        #f1 = f.seek(pos).read()
        #f.close()

        #self.send = io.BytesIO( head + f1 )

        #while f := send.read(8):
            #req.send(self.send)
            #x+=1
#            if time.time() >= (aa + 1):
#                print(str(x)," octects /sec")
#                if int(x) < 1000000:
#                    self.msgmypool.put(["slow",req.getpeername(),self.finhead,self.filepath+'/'+self.file,x])
#                    self.msgmypool.put(["slow",self.req])
#                    time.sleep(30)

#                x=0
#                aa = time.time()

    def extpool_srv(self):
        pass
    def extpool_clt(self,pairs):
        pass


