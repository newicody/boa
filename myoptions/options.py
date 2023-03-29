class myoptions:
    def __init__(self,name,conf=False,timing=False,venv_path=False,ssl=False,ssl_file=False,port=False,interface=False,dhcp=False,ip=False,log=False,pool=False,macaddress=False,github=False,init=False,boot=False,user=False):
        self.name = name
        self.opt = []
        self.conf=conf

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
        self.boot=boot
        self.github=github
        self.user=user

    def assign(self):
        for elt in self.opt:
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
            if elt[0] == "boot":
                self.boot = elt[1]
            if elt[0] == "user":
                self.user = elt[1]

    def newpart(self):
        self.opt.append(["venv_path",self.venv_path])
        self.opt.append(["port",self.port])
        self.opt.append(["interface",self.interface])
        self.opt.append(["ssl",self.ssl])
        self.opt.append(["ssl_file",ssl_file])
        self.opt.append(["timing",self.timing])
        self.opt.append(["dhcp",self.dhcp])
        self.opt.append(["log",self.log])
        self.opt.append(["macaddress",self.macaddress])
        self.opt.append(["pool",self.pool])
        self.opt.append(["github",self.github])
        self.opt.append(["ip",self.ip])
        self.opt.append(["user",self.user])
        self.opt.append(["boot",self.boot])

    def writeconfig(self):
        print(self.conf)
        fichier = open(self.conf, "a")
        fichier.write("\n[" + self.name + "]\n")
        for elt in self.opt:
            fichier.write(elt[0] + " = " + elt[1] + "\n")
        fichier.write("\n")
        fichier.close()

    def configvenv(self):
        pass
    def configinitinit(self):
        pass
