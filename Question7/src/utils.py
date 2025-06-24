# question7/src/utils.py
import os
import configparser

def get_config():
    config = configparser.ConfigParser()
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config.config')
    config.read(config_path)
    return config
