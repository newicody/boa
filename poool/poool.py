import multiprocessing

class poool:
    def __init__(self,manager):
        self.messages_pool  = manager.Queue()
    def mainprocess(self):
        while True:
            new_value = self.messages_pool.get()
            print(new_value)

    def local_client_pool(self):
        pass

    def local_client_server(self):
        pass
    def ext_client_pool(self):
        pass

    def ext_client_server(self):
        pass

