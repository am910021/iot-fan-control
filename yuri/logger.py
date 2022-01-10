

class Logger:
    _instance = None
    
    DEBUG       = 0
    INFO        = 1
    WARNING     = 2
    ERROR       = 3

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            pass
            #raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            Logger._instance = self
            self._levels = [Logger.INFO]
    
    def get_id(self):
        return self._id
    
    def setLevels(self, levels:list):
        self._levels = levels
    
    def debug(self,message, *args, **kwargs):
        if not Logger.DEBUG in self._levels:
            return
        print('[Debug] '+message.format(*args, **kwargs))
    
    def info(self,message, *args, **kwargs):
        if not Logger.INFO in self._levels:
            return
        print('[Info] '+message.format(*args, **kwargs))
        
    def warning(self,message, *args, **kwargs):
        if not Logger.WARNING in self._levels:
            return
        print('[Warning] '+message.format(*args, **kwargs))
    
    def error(self,message, *args, **kwargs):
        if not Logger.ERROR in self._levels:
            return
        print('[Error] '+message.format(*args, **kwargs))
        
logger = Logger.get_instance()
