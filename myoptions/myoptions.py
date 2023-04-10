import os
import subprocess
import difflib

class myoptions:
    def __init__(self,name,conf=False,timing=False,venv_path=False,ssl=False,ssl_file=False,port=False,interface=False,ip=False,log=False,github=False,init=False,boot=False,user=False,poopool=False):
        self.name = name
        self.opt = []
        self.conf=conf

        self.init = init
        self.boot = boot
        self.user = user
        self.timing=timing
        self.venv_path=venv_path
        self.ssl=ssl
        self.ssl_file=ssl_file
        self.port=port
        self.interface=interface
        self.ip=ip
        self.log=log
        self.github=github
        self.poopool=poopool

    def assign(self):
        for elt in self.opt:
            if elt[0] == "init":
                self.init = elt[1]
            if elt[0] == "boot":
                self.boot = elt[1]
            if elt[0] == "user":
                self.user = elt[1]
            if elt[0] == "venv_path":
                self.venv_path = elt[1]
            if elt[0] == "port":
                self.port = elt[1]
            if elt[0] == "interface":
                self.interface = elt[1]
            if elt[0] == "ssl":
                self.ssl = elt[1]
            if elt[0] == "ssl_file":
                self.ssl_file = elt[1]
            if elt[0] == "timing":
                self.timing = elt[1]
            if elt[0] == "log":
                self.log = elt[1]
            if elt[0] == "github":
                self.github = elt[1]
            if elt[0] == "ip":
                self.ip = elt[1]
            if elt[0] == "poopool":
                self.poopool = elt[1]

    def localpool_newpart(self):
        self.opt.append(["localpool_user",self.user])
        self.opt.append(["localpool_port",self.port])
        self.opt.append(["localpool_interface",self.interface])
        self.opt.append(["localpool_ssl",self.ssl])
        self.opt.append(["localpool_ssl_file",self.ssl_file])
        self.opt.append(["localpool_timing",self.timing])
        self.opt.append(["localpool_log",self.log])
        self.opt.append(["localpool_ip",self.ip])
        self.opt.append(["localpool_boot",self.boot])

    def wwwpool_newpart(self):
        self.opt.append(["wwwpool_user",self.user])
        self.opt.append(["wwwpool_port",self.port])
        self.opt.append(["wwwpool_interface",self.interface])
        self.opt.append(["wwwpool_ssl",self.ssl])
        self.opt.append(["wwwpool_ssl_file",self.ssl_file])
        self.opt.append(["wwwpool_timing",self.timing])
        self.opt.append(["wwwpool_log",self.log])
        self.opt.append(["wwwpool_ip",self.ip])
        self.opt.append(["wwwpool_boot",self.boot])
        self.opt.append(["wwwpool_pool",self.poopool])

    def newpart(self):
        self.opt.append(["user",self.user])
        self.opt.append(["venv_path",self.venv_path])
        self.opt.append(["port",self.port])
        self.opt.append(["interface",self.interface])
        self.opt.append(["ssl",self.ssl])
        self.opt.append(["ssl_file",self.ssl_file])
        self.opt.append(["timing",self.timing])
        self.opt.append(["log",self.log])
        self.opt.append(["github",self.github])
        self.opt.append(["ip",self.ip])
        self.opt.append(["boot",self.boot])
        self.opt.append(["pool",self.poopool])






    def writeconfig(self):
        print(self.conf + " va être édité :")
        with open(self.conf) as file_1:
            file_1_text = file_1.readlines() 
        a=""
        for elt in self.opt:
            a = a + elt[0] + " = " + str(elt[1]) + "\n"
        out = "".join(file_1_text) + "\n[" + self.name + "]\n" + a
        
        inf = "".join(file_1_text)
        for line in difflib.unified_diff(inf.split("\n"), out.split("\n"), fromfile="origin "+self.conf,tofile='new '+self.conf,n=9999):
            print(line)

        print("On continue ? (say 'y')")
        really = input()
        if really != "y":
            exit()


        fichier = open(self.conf, "a")
        fichier.write("\n[" + self.name + "]\n")
        for elt in self.opt:
            fichier.write(elt[0] + " = " + str(elt[1]) + "\n")
        fichier.write("\n")
        fichier.close()

    def writeconfigpool(self):
        print(self.conf + " va être édité :")

        newfile = []
        finde = False
        fichier1 = open(self.conf, "r")
        lines = fichier1.readlines()

        for line in lines:
            sline = line.strip()
            if finde == True and line[0] == "[":
                for elt in self.opt:
                    newfile.append(elt[0] + " = " + str(elt[1]) + "\n")
                finde = False
            if sline ==  "["+self.name+"]":
                finde=True
            newfile.append(line)
        fichier1.close()

        inf="".join(lines)
        out="".join(newfile)
        for line in difflib.unified_diff(inf.split("\n"), out.split("\n"), fromfile="origin "+self.conf,tofile='new '+self.conf,n=9999):
            print(line)

        print("On continue ? (say 'y')")
        really = input()
        if really != "y":
            exit()

        outfile = open(self.conf, 'w')
        for elt in newfile:
            outfile.write(elt)
        outfile.close()

    def search_venv(self):
        if os.path.exists(self.venv_path):
            return True
        else:
            return False

    def configvenv(self):
        try:
            os.mkdir(self.venv_path)
        except FileExistsError:
            print("path exist, venv abordead")
            exit()
        except PermissionError:
            print("permission error, venv abordead")

        subprocess.run(['python3.11',"-m","venv", self.venv_path])

    def configinitinit(self,myinit,tpool=False):
        ''' configuration '''
        '''/etc/systemd/system/ – pour que le service s’exécute au démarrage du système'''
        '''/etc/systemd/user/ – service qui s’exécute à la connexion de n’importe quel utilisateur'''
        '''~/.config/systemd/user/ – pour que le service s’exécute à la connexion d’un utilisateur spécifique'''
        print("Your selected init is : "+ myinit.init)

        if myinit.init == "systemd":
            print(self.boot)
            if self.boot == "system":
                systemd_path = "/etc/systemd/system/"
            elif self.boot == "users":
                systemd_path = "/etc/systemd/user/"
            elif  self.boot == "user":
                systemd_path = "/home/" + self.user + "/.config/systemd/user/"
                try:
                    os.makedirs(systemd_path, exist_ok=True)
                except:
                    print("rep error")
            else:
                print("erreure pendant la creation du service systemd")
                exit()

            if tpool==False:
                fle="boa@.service"
            elif tpool=="localpool":
                fle="boalocalpool.service"
            elif tpool=="wwwpool":
                fle="boawebpool.service"

            fichier = open(systemd_path + fle, "w")
            fichier.write("[Unit]\n\
Description=script description %I \n\
[Service]\n\
Type=simple\n\
ExecStart=python3.11 /home/newic/git/main.py -R /home/newic/git/conf/boa.conf -n %i \n\
# Restart=on-failure\n\
[Install]\n\
WantedBy=multi-user.target\n\
")
            fichier.close()
