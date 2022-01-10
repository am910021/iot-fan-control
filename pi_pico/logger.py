
class Logger:
    def __init__(self, dev):
        self.dev=dev
    
    
    def info(self, string):
        if self._dev:
            print(string)