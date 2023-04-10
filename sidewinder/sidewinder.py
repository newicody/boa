from new_socket.new_socket import *
from socket_chield.socket_chield import *
import threading
import asyncio


class sidewinder:
    def __init__(self,port_value,path_value,timetowait,interface,ip,myerrors,mylog,mypool,ssl=False,ssl_file=False):
        self.port_value = int(port_value)
        self.path_value = path_value
        self.timetowait = timetowait
        self.interface = interface
        self.ip = ip
        self.ssl = ssl
        self.ssl_file = ssl_file

        self.messages_err = myerrors.messages_err
        self.messages_log = mylog.messages_log
        self.messages_pool = mypool.messages_pool

    def fire(self):
        root = new_socket(self.port_value,self.path_value,self.timetowait,self.interface,self.ip,self.ssl,self.ssl_file)
        chield = []
        send = []


        while True:
            #self.messages_err.put("this is an error")
            #self.messages_log.put("this is a log")
            #self.messages_pool.put("this is a pool msg")

            root.read_chield(self.timetowait)
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

                    send.append(threading.Thread(target=chield[-1].response))
                    send[-1].start()
                    self.messages_log.put("connection")
            x=0
            for elt in send:
                if elt.is_alive() == False:
                    root.list_clients[x].close()
                x+=1
