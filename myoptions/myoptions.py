import os
import subprocess

class myoptions:
    def __init__(self,name,conf=False,timing=False,venv_path=False,ssl=False,ssl_file=False,port=False,interface=False,dhcp=False,ip=False,log=False,pool=False,macaddress=False,github=False,init=False,boot=False,user=False):
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
        self.dhcp=dhcp
        self.ip=ip
        self.log=log
        self.pool=pool
        self.macaddress=macaddress
        self.github=github

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
            if elt[0] == "dhcp":
                self.dhcp = elt[1]
            if elt[0] == "log":
                self.log = elt[1]
            if elt[0] == "macaddress":
                self.macaddress = elt[1]
            if elt[0] == "pool":
                self.pool = elt[1]
            if elt[0] == "github":
                self.github = elt[1]
            if elt[0] == "ip":
                self.ip = elt[1]
    def newpart(self):
        self.opt.append(["user",self.user])
        self.opt.append(["venv_path",self.venv_path])
        self.opt.append(["port",self.port])
        self.opt.append(["interface",self.interface])
        self.opt.append(["ssl",self.ssl])
        self.opt.append(["ssl_file",self.ssl_file])
        self.opt.append(["timing",self.timing])
        self.opt.append(["dhcp",self.dhcp])
        self.opt.append(["log",self.log])
        self.opt.append(["macaddress",self.macaddress])
        self.opt.append(["pool",self.pool])
        self.opt.append(["github",self.github])
        self.opt.append(["ip",self.ip])
        self.opt.append(["boot",self.boot])

    def writeconfig(self):
        print(self.conf)
        fichier = open(self.conf, "a")
        fichier.write("\n[" + self.name + "]\n")
        for elt in self.opt:
            fichier.write(elt[0] + " = " + str(elt[1]) + "\n")
        fichier.write("\n")
        fichier.close()

    def configvenv(self):
        try:
            os.mkdir(self.venv_path)
        except FileExistsError:
            print("path exist, venv abordead")
            exit()
        except PermissionError:
            print("permission error, venv abordead")

        subprocess.run(['python3.11',"-m","venv", self.venv_path])

    def configinitinit(self,myinit):
        ''' configuration '''
        '''/etc/systemd/system/ – pour que le service s’exécute au démarrage du système'''
        '''/etc/systemd/user/ – service qui s’exécute à la connexion de n’importe quel utilisateur'''
        '''~/.config/systemd/user/ – pour que le service s’exécute à la connexion d’un utilisateur spécifique'''
        print("Your selected init is : "+ myinit.init)

        if myinit.init == "systemd":
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
                exit()
            fichier = open(systemd_path + "boa@.service", "w")
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
