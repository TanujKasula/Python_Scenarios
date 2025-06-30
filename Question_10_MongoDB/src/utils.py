import configparser
import os
import urllib.parse
from pymongo import MongoClient
import urllib
from sqlalchemy import create_engine

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    config_path=os.path.join(base_path,'config','config.config')
    config.read(config_path)
    return config

def get_mongo_client():
    config=get_config()
    host=config['MONGODB']['host']
    port=config['MONGODB']['port']
    client=MongoClient(f"mongodb://{host}:{port}")
    return client


def get_sql_engine():
    config=get_config()
    sql=config['SQL_SERVER']
    connection_string=f"""
                            DRIVER={{{sql['driver']}}};
                            SERVER={sql['server']};
                            DATABASE={sql['database']};
                            UID={sql['username']};
                            PWD={sql['password']};
                            TrustServerCertificate=yes;
                        """
    params=urllib.parse.quote_plus(connection_string)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine
