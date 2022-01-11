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
        self.default_is_loaded=False
        if self.has_config_file():
            self.load_config()
        else:
            self.load_default()
        gc.collect()

    def get_id(self):
        return self._id

    def load_default(self):
        self.http['debug'] = False
        self.http['address'] = '0.0.0.0'
        self.http['port'] = 80
        self.http['timeout'] = 15
        self.http['require_auth'] = False
        self.http['realm'] = "esp"
        self.http['user'] = "admin"
        self.http['password'] = ""
        self.http['max_headers'] = 10
        self.http['max_content_length'] = 1024

        self.ap['enable'] = True
        self.ap['ssid'] = ''
        self.ap['password'] = ''

        self.wifi['enable'] = False
        self.wifi['ssid'] = ''
        self.wifi['password'] = ''
        self.default_is_loaded=True

    def has_config_file(self):
        folders = os.listdir()
        return 'config.txt' in folders

    def save_config(self):
        setting = {}
        setting['http'] = self.http
        setting['ap'] = self.ap
        setting['wifi'] = self.wifi
        with open('config.txt', 'w') as jsonfile:
            json.dump(setting, jsonfile)

    def load_config(self):
        try:
            with open('config.txt', 'r') as jsonfile:
                data = json.load(jsonfile)
                http = data['http']
                ap = data['ap']
                wifi = data['wifi']

                self.http['debug'] = http['debug'] is True
                self.http['address'] = http['address']
                self.http['port'] = int(http['port'])
                self.http['timeout'] = int(http['timeout'])
                self.http['require_auth'] = http['require_auth'] is True
                self.http['realm'] = http['realm']
                self.http['user'] = http['user']
                self.http['password'] = http['password']
                self.http['max_headers'] = int(http['max_headers'])
                self.http['max_content_length'] = int(http['max_content_length'])

                self.ap['enable'] = ap['enable'] is True
                self.ap['ssid'] = ap['ssid']
                self.ap['password'] = ap['password']

                self.wifi['enable'] = wifi['enable'] is True
                self.wifi['ssid'] = wifi['ssid']
                self.wifi['password'] = wifi['password']
                gc.collect()
        except IndexError:
            raise Exception('The config.txt key/value attribute is wrong, please check the file or delete it.')


config = Config.get_instance()
