class Logger:
    _instance = None

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            raise Exception('only one instance can exist')

        self._id = id(self)
        Logger._instance = self
        self._levels = [Logger.ERROR]

    def get_id(self):
        return self._id

    def set_levels(self, levels: list):
        self._levels = levels

    def debug(self, message, *args, **kwargs):
        self.print(Logger.DEBUG, '[Debug] ' + message.format(*args, **kwargs))

    def info(self, message, *args, **kwargs):
        self.print(Logger.INFO, '[Info] ' + message.format(*args, **kwargs))

    def warning(self, message, *args, **kwargs):
        self.print(Logger.WARNING, '[Warning] ' + message.format(*args, **kwargs))

    def error(self, message, *args, **kwargs):
        self.print(Logger.ERROR, '[Error] ' + message.format(*args, **kwargs))

    def print(self, Level, msg):
        if not Level in self._levels:
            return
        print(msg)


logger = Logger.get_instance()
