import configparser
import os
from .config import Configuration
config = Configuration()

path = os.getcwd()
config_file = path + '/config/permission.ini'


class Permission:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        self.sections = config.sections()
        self.permitted = self.create_group()

    def create_group(self):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        group = {}

        for section_name in self.sections:
            section_options = config.options(section_name)
            group[section_name] = {}
            for option in section_options:
                option_value = config.get(section_name, option)
                group[section_name][option] = option_value.split()

        return group

    def create_whitelist(self, role):
        whitelist = {}

        for i in self.permitted:
            if role in i:
                for key in self.permitted[role]:
                    if 'commandwhitelist' in key:
                        whitelist = self.permitted[role][key]

        return whitelist

    def check_command(self, role, command):
        whitelist = self.create_whitelist(role)
        has_permission = False

        for i in whitelist:
            if command in i:
                has_permission = True

        return has_permission
