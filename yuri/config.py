import os, gc, json


class Config:
    _instance = None

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config()
        return Config._instance

    def __init__(self):
        if Config._instance is not None:
            raise Exception('only one instance can exist')

        self._id = id(self)
        Config._instance = self
        self.http = {}
        self.ap = {}
        self.wifi = {}
        if self.hasConfig2File():
            self.loadConfig()
        else:
            self.loadDefault()
            self.saveConfig()
        gc.collect()

    def get_id(self):
        return self._id

    def loadDefault(self):
        self.dev_mode = True

        self.http['bind_addr'] = '0.0.0.0'
        self.http['port'] = 80
        self.http['timeout'] = 15
        self.http['require_auth'] = False
        self.http['realm'] = "esp8266"
        self.http['user'] = "admin"
        self.http['password'] = "uhttpD"
        self.http['max_headers'] = 10
        self.http['max_content_length'] = 1024

        self.ap['enable'] = True
        self.ap['essid'] = 'esp8266'
        self.ap['password'] = '0123456789'

        self.wifi['enable'] = False
        self.wifi['essid'] = ''
        self.wifi['password'] = ''

    def hasConfig2File(self):
        folders = os.listdir()
        return 'config.txt' in folders

    def saveConfig(self):
        setting = {}
        setting['dev_mode'] = self.dev_mode
        setting['http'] = self.http
        setting['ap'] = self.ap
        setting['wifi'] = self.wifi
        with open('config.txt', 'w') as jsonfile:
            json.dump(setting, jsonfile)

    def loadConfig(self):
        try:
            with open('config.txt', 'r') as jsonfile:
                data = json.load(jsonfile)
                self.dev_mode = data['dev_mode'] is True
                http = data['http']
                ap = data['ap']
                wifi = data['wifi']

                self.http['bind_addr'] = http['bind_addr']
                self.http['port'] = int(http['timeout'])
                self.http['timeout'] = int(http['timeout'])
                self.http['require_auth'] = http['require_auth'] is True
                self.http['realm'] = http['realm']
                self.http['user'] = http['user']
                self.http['password'] = http['password']
                self.http['max_headers'] = int(http['max_headers'])
                self.http['max_content_length'] = int(http['max_content_length'])

                self.ap['enable'] = ap['enable'] is True
                self.ap['essid'] = ap['essid']
                self.ap['password'] = ap['password']

                self.wifi['enable'] = wifi['enable'] is True
                self.wifi['essid'] = wifi['essid']
                self.wifi['password'] = wifi['password']
                gc.collect()
        except:
            raise Exception('The config.txt key/value attribute is wrong, please check the file or delete it.')


config = Config.get_instance()

