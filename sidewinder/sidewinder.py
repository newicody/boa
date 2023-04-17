from new_socket.new_socket import *
from socket_chield.socket_chield import *
import threading
import asyncio


class sidewinder:
    def __init__(self,port_value,path_value,timetowait,interface,ip,peers,ssll=False,ssl_file=False):
        self.port_value = int(port_value)
        self.path_value = path_value
        self.timetowait = timetowait
        self.interface = interface
        self.ip = ip
        self.ssll = ssll
        self.ssl_file = ssl_file

        self.peers = peers



    def fire(self,myerrors,mylog,mypool):

        self.msgerr = myerrors.messages_err
        self.msgpool = mypool.messages_pool
        self.msglog = mylog.messages_log

        root = new_socket(self.port_value,self.path_value,self.timetowait,self.interface,self.ip,self.ssll,self.ssl_file)
        chield = []
        send = []

        while True:
            if len(mypool.problems) > 0:
                 print("anomalie detectée")
                 a = mypool.problems.pop(0)
                 mypool.localpool_clt(a)

            root.read_chield(self.timetowait)
            root.connect()
            root.processing()
            if( root.clienttoread != []):
                for elt in root.clienttoread:
                    chield.append(socket_chield(elt,myerrors,mylog,mypool,root.path))
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


                    send.append(threading.Thread(target=chield[-1].response(self.msgpool)))
                    send[-1].start()

            x=0
            for elt in send:
                if elt.is_alive() == False:
                    root.list_clients[x].close()
                x+=1

