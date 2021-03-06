import configparser
import os

path = os.path.abspath('')
config_file = os.path.join(path, 'config', 'config.ini')
example_config = os.path.join(path, 'config', 'example-config.ini')


class Configuration():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        self.prefix = config.get('Chat', 'prefix')
        self.token = config.get('Credentials', 'token')
        self.ownerid = config.get('Permission', 'ownerid')
        self.permitted = config.get('Permission', 'permitted')
        self.logchannel = config.get('Channel', 'logchannel')
