import configparser
import os

path = os.path.dirname(os.path.abspath(__file__))
config_file = path + '/config/config.ini'


class Configuration():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        self.prefix = config.get('Chat', 'prefix')
        self.token = config.get('Credentials', 'token')
        self.ownerid = config.get('Permission', 'ownerid')
        self.permitted = config.get('Permission', 'permitted')
