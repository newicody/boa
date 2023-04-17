from myoptions import myoptions
class config_parse:
    def __init__(self,fichier,name):
        
        self.fichier = fichier

        if name != False:
            self.name=name

        self.op()

        self.options_init = ["init","boot"]
        self.options_server = ["port","venv_path","interface","ssll","ssl_file","timing","ip","log","github","token","user","poopool"]

        a = self.parse()
        test=[]
        for elt in a:
            if elt!=['']:
                test.append(elt)
        self.config=[]
        self.stage2(test)

    def op(self):
        file = open(self.fichier,"r")
        self.content = file.readlines()
        file.close()

    def parse(self):
        part = False
        for elt in self.content:
            if part == True and elt[0]== "[":
                value = elt.split("\n")[0].split("#")[0]
                yield [value[1:len(value)-1]]
            elif elt[0] != "#" and elt[0]=="[" and part == False:
                value = elt.split("\n")[0].split("#")[0]
                if value[0] == "[" and value[-1] == "]":
                    yield [value[1:len(value)-1]]
                part = True
            elif elt[0] != "#" and part == True:
                yield elt.split("\n")[0].split(" #")[0].split(" = ")


    def stage2(self,test):
        for elt in test:
            if len(elt) == 1:
                self.config.append(myoptions.myoptions(elt))
            elif len(elt) == 2:
                if self.config[-1].name == ["init"]:
                    for elt2 in self.options_init:
                        if elt2 == elt[0]:
                            self.config[-1].opt.append(elt)
                else:
                    for elt2 in self.options_server:
                        if elt2 == elt[0]:
                            self.config[-1].opt.append(elt)
