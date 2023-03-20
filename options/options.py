class options:
    def __init__(self,name):
        self.name = name
        self.opt = []
        
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
