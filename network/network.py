import difflib
from subprocess import run
class network:
    def __init__(self,interface,ip,ssl,port,config_file="/etc/network/interfaces"):
        self.interface = interface
        self.ip = ip
        self.ssl = ssl
        self.port = port

        self.config_file = config_file

        file = open(self.config_file,"r")
        self.content = file.readlines()
        file.close()

        self.slot = None

        self.value = []

        self.sources = []

        self.cur_conf = ""
        self.new_elt = [["auto",self.interface],\
["iface",self.interface,"inet","static"],\
["address",self.ip],\
["netmask","255.255.255.0"],\
["gateway","192.168.1.254"]]


        for elt in self.content:
            if elt[0] != "#":
                a = elt.split("\n")[0].split("#")[0].split(' ')
                a = ' '.join(a).split()
                if a != []:
                    self.value.append(a)

    def search(self,motif=["source","auto"]):
        for elt in self.value:
            for elt2 in motif:
                if elt[0] == elt2:
                    yield elt

    def search_params(self,start=["iface"],end=["iface","auto","source"]):
        result = []
        for elt0 in self.value:
            ending = False
            starting = False
            continu = True
            for elt33 in end:
                if elt33 == elt0[0]:
                   ending = True

            for elt in start:
                if elt == elt0[0]:
                   starting = True

            if continu == True and starting == True and ending == True:
                result.append([elt0])
                continu = True

            elif continu == True and starting == False and ending == False:
                result[-1].append(elt0)
                continu = False
        yield result

    def search_same_ip(self):
        for elt in self.search_params():
            for elt2 in elt:
                if elt2[1][0] == "address" and elt2[1][1] == self.ip:
                    return True

    def search_virtual(self,ifname,motif="iface"):
        t=[]
        x = len(ifname) + 1
        for elt in self.value:
            if elt[0] == motif and elt[1].split(":")[0] == ifname:
                if elt[1][x:] != "" :
                    t.append(int(elt[1][x:]))
        z=0
        y=0
        while z<len(t):
            for elt in t:
                if elt == y:
                    y+=1
                    continue
                else:
                    z+=1
        self.slot=y

    def readconf(self):
        for elt in self.search(["source"]):
            yield ' '.join(elt)
        for elt in self.search(["auto"]):
            yield ' '.join(elt)
            for elt2 in self.search_params():
                for el3 in elt2:
                    if elt[1] == el3[0][1]:
                        for elt4 in el3:
                            yield ' '.join(elt4)
    def modconf(self):
        self.new_elt[0][1] = self.interface + ":" + str(self.slot)
        self.new_elt[1][1] = self.interface + ":" + str(self.slot)
        self.new_elt[2][1] = self.ip

        for elt in self.new_elt:
            yield ' '.join(elt)


    def writeconf(self):
        inf="".join(self.content)

        out = ""
        for elt in self.cur_conf:
            out = out + (elt+"\n")
        for elt in self.new_elt2:
            out = out + (elt+"\n")

        for line in difflib.unified_diff(inf.split("\n"), out.split("\n"), fromfile="origin "+self.config_file,tofile='new '+self.config_file,n=9999):
            print(line)

        print("On continue ? (say 'y')")
        really = input()
        if really != "y":
            exit()

        file = open(self.config_file,"w")
        file.write(out)
        file.close()

    def upforever(self):
         run(["ifup", self.interface + ":" + str(self.slot)])


