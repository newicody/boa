import multiprocessing

class errors:
    def __init__(self,manager):
        self.messages_err = manager.Queue()

    def mainprocess(self):
        while True:
            new_value = self.messages_err.get()
            print(new_value)
