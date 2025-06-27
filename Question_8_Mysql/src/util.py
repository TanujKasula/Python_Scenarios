import urllib
import configparser
import urllib.parse
from sqlalchemy import create_engine
import pandas as pd
import os

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.join(os.path.dirname(__file__),'..')
    config_path=os.path.join(base_path,'config','config.config')
    config.read(config_path)
    return config

def my_sql_engine():
    config=get_config()
    my_sql=config['MYSQL']
    encoded_password=urllib.parse.quote_plus(my_sql['password'])
    connectionstring=f"mysql+mysqlconnector://{my_sql['user']}:{encoded_password}@{my_sql['host']}:{my_sql['port']}/{my_sql['database']}"
    return create_engine(connectionstring)

def sql_server_engine():
    config=get_config()
    ms_sql=config['SQL_SERVER']
    connectionstring=f"""
                        DRIVER={{{ms_sql['driver']}}};
                        SERVER={ms_sql['server']};
                        DATABASE={ms_sql['database']};
                        UID={ms_sql['username']};
                        PWD={ms_sql['password']};
                        TrustServerCertificate=yes;
                    """
    params=urllib.parse.quote_plus(connectionstring)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
