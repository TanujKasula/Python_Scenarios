import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy import inspect
import urllib
import pandas as pd

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    config_path=os.path.join(base_path,'config','config.config')
    config.read(config_path)
    return config

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

def table_exists(engine,table_name):
    inspector=inspect(engine)
    return inspector.has_table(table_name)