

class Log:
    
    DEBUG       = 'debug'
    INFO        = 'info'
    WARNING     = 'warning'
    ERROR       = 'error'
    
    def __init__(self, config, name = "unknown") :
        '''Constructor'''
        self._sinks = self.load_sinks(config)
        self._levels = config['levels']
        self._name = config['name']
        
    def debug(self, format_str, *args) :
        '''Send a debug log message'''
        self.log(self.DEBUG, format_str, *args)

    def info(self, format_str, *args) :
        '''Send an info log message'''
        self.log(self.INFO, format_str, *args)

    def warning(self, format_str, *args) :
        '''Send a warning log message'''
        self.log(self.WARNING, format_str, *args)

    def error(self, format_str, *args) :
        '''Send an error log message'''
        self.log(self.ERROR, format_str, *args)
        
    def log(self, level, format_str, *args) :
        if level in self._levels :
            try :
                message = self.create(level, format_str, *args)
            except Exception :
                print("WARNING: Error formatting log message.  Log will be delivered unformatted.")
                sys.print_exception(e)
                message = (level, format_str, args)
            for name, sink in self._sinks.items() :
                self.do_log(sink, message)