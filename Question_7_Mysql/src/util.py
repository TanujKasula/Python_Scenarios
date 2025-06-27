import configparser
import os
import json
from datetime import datetime

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    config_path=os.path.join(base_path,'config.config')
    config.read(config_path)
    return config

def get_metadata_file():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),'..','etl_metadata.json'))

def read_last_loaded_date(table_name):
    file=get_metadata_file()
    if not os.path.exists(file):
        return None
    with open(file,'r') as f:
        metadata=json.load(f)
    return metadata.get(table_name)


def update_last_loaded_date(table_name,new_date):
    file=get_metadata_file()
    if os.path.exists(file):
        with open(file,'r') as f:
            metadata=json.load(f)
    else:
        metadata={}

    metadata[table_name]=new_date.strftime('%Y-%m-%d %H:%M:%S')
    with open(file,'w') as f:
        json.dump(metadata,f,indent=4)