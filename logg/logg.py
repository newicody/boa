import multiprocessing

class logg:
    def __init__(self,manager):
        self.messages_log = manager.Queue()

    def mainprocess(self):
        while True:
            new_value = self.messages_log.get()
            print(new_value)
