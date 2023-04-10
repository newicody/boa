import os
import io
import time
class socket_chield:
    def __init__(self,req,authorized_path):
        self.req = req
        self.state="connected"
        self.close=0
        self.path = authorized_path

        self.index = ["index.php","index.html"]

        self.listing = None

        self.ressources = "res"


    def recept(self):
        self.msg = self.req.recv(1024).decode("utf-8")
        self.state="requested"
        print(self.msg)
        self.armor = self.msg.split('\r')[0].split(' ')
        self.type = self.armor[0] # GET ...
        self.option = self.armor[1] # /xx/xxx/xxx/x.xxx
        #print(self.type)

    def valid_path(self):
        if self.option =="/":
            self.filepath = self.path # (self.path = root)
            self.file=None
            self.fileext=None

        elif self.option[-1]=="/": #and len(self.option)>1:
            self.outpath = self.option[1::]
            self.filepath = self.path+self.option[1::]
            self.file=None
            self.fileext=None

        else:
            self.filepath = self.option.split("/")
            self.filepath.pop(0)
            self.file = self.filepath.pop(-1)

            if len(self.file.split('.'))>1: 
                self.fileext = self.file.split('.')[1]
            else:
                self.fileext = None

            self.filepath = '/'.join(self.filepath)
            self.filepath = self.path + ''.join(self.filepath)

        self.state = "path completed"

    def valid_file(self):
        if self.fileext != None:
            if len(self.fileext.split('php?'))>1:
                self.phparg=self.fileext.split('php?')[0].split("&")
                self.fileext="php"
            else:
                self.phparg=None
        self.state = "extension verified"

    def path_accesible(self):

        if os.path.exists(self.filepath) is False:
            print("erreur accessing pa0th")
            self.filepath = self.path + '/errors/'
            self.file="404.html"
            self.mime = "text/html"
            self.fileext="html"

        self.state="path access verified"

    def add_defaut_index(self):
        for elt in os.listdir(self.filepath):
            for elt2 in self.index:
                if elt == elt2:
                    self.file = elt
                    self.fileext = elt.split(".")[1]
                    self.listing = None
                    return

        self.listing = os.listdir(self.filepath)
        self.file = "listing.php"
        self.filepath = self.path + self.ressources
        
        self.fileext = "php"


    def file_accesible(self):
        try:
            with open(self.filepath+'/'+self.file): pass
        except IOError:
            print("le fichier nexiste pas ou vous n'avez pas la permission pour y acceder en lecture")
            self.filepath = self.path + '/errors/'
            self.file="404.html"
            self.mime = "text/html"
            self.fileext="html"
        self.state = "access verified"


    def mime_detect(self):
        self.php = False
        if (self.type == "GET"):
            if (self.fileext == "php"):
                self.mime = "text/html"
                self.php = True
            elif (self.fileext == "html"):
                self.mime = "text/html"
            elif (self.fileext == "txt"):
                self.mime = "text/html"
            elif (self.fileext == "js"):
                self.mime = "text/javascript"
            elif (self.fileext == "ico"):
                self.mime = "image/x-icon"
            elif (self.fileext == "bin"):
                self.mime = "application/octet-stream"
            elif (self.fileext == None):
                self.mime = "application/octet-stream"
            else:
                self.mime = "text/html"

        elif (self.type == "POST"):
            if (self.fileext == "php"):
                self.mime = "text/html"
                self.php = True
        self.state = "analyzed"

    def php_args(self):
        #self.getphparg = self.phparg
        self.postphparg = ""
        if self.listing == None and self.msg.split("\n")[-1] != "":
            self.postphparg = " dest " + self.filepath + '/' + self.file
            for elt,elt2 in json.loads(self.msg.split("\n")[-1]).items():
                self.postphparg +=  " " + elt + " " + elt2
        elif (self.listing == None):
            self.postphparg = " dest " + self.filepath +"/"+ self.file


        elif self.listing != None:
            self.postphparg = " dest " + self.filepath + "/" + self.file + " path " + self.outpath
            x=0
            for elt in self.listing:
                self.postphparg += " " + str(x) + " " + elt
                x+=1
            print(self.postphparg)

        self.state = "arguments readed"

    def mime_php(self):
        self.f1 = bytes(os.popen(rf"php " + self.path + "res/" + "wrapper.php " + self.postphparg ).read(),'utf-8')
        self.php = False
        self.state = "php accessed"

    def mime_text(self):
        try:
            self.f2 = open(self.filepath+'/'+self.file,"rb")
            self.f1 = self.f2.read()
            self.f2.close()
        except:
            self.f1 = bytes("Fichier introuvable et impossible d'accéder à la page d'erreur explicite.", "utf-8")
        self.state = "Text accessed"

    def create_header(self):
        self.header = 'HTTP/1.1 200 OK\n'
        self.mimetype = self.mime
        self.header += 'Content-Type: '+ str(self.mimetype) + '\n'
        self.header += 'Content-Length: ' + str(len(self.f1)) + '\n\n'
        self.finhead = bytes(self.header,'utf-8')
        self.state = "header created"

    def create_final_io(self):
        self.send = io.BytesIO( self.finhead + self.f1 )
        self.state = "finalized"
    def response(self):
        x=0
        aa = time.time()
        while f := self.send.read(8):
            self.req.send(f)
            x+=1
            if time.time() >= (aa + 1):
                print(str(x)," octects /sec")
                if int(x) < 1000000:
                    pass 

                x=0
                aa = time.time()
        self.state = "transfered"
        self.close = 1
