import os
import configparser
from sqlalchemy import create_engine
import urllib
from pymongo import MongoClient

def get_config():
    config = configparser.ConfigParser()
    base_path = os.path.dirname(__file__)
    config.read(os.path.join(base_path, '..', 'config', 'config.config'))
    return config

def get_mongo_client():
    config=get_config()
    host=config['MONGODB']['host']
    port=config['MONGODB']['port']
    client=MongoClient(f"mongodb://{host}:{port}")
    return client

def get_sqlserver_engine():
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
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def get_mysql_engine():
    config=get_config()
    mysql=config['MYSQL']
    encodedpassword=urllib.parse.quote_plus(mysql['password'])
    connectionString=f"mysql+mysqlconnector://{mysql['user']}:{encodedpassword}@{mysql['host']}:{mysql['port']}/{mysql['database']}"
    return create_engine(connectionString)
