import socket
import select

class new_socket:
    def __init__(self,port,path,timetowait,interface,ip):
        self.hote = ip
        self.port = port
        self.path = path
        self.interface=interface

        self.connection = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.connection.bind((self.hote,self.port))
        self.connection.listen(10)
        self.connection.setsockopt(socket.SOL_SOCKET, 25, self.interface.encode('utf-8'))
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
        self.clients_attentes, self.wlist, self.xlist = select.select([self.connection], [], [], float(self.timetowait))
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

