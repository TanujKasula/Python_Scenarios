import os
import configparser
import pyodbc
from sqlalchemy import create_engine

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.dirname(__file__)
    config_path=os.path.join(base_path,'config.config')
    config.read(config_path)
    return config

def get_sql_con():
    config=get_config()
    sql=config["SQL_SERVER"]
    connectionstring=f"""
                        DRIVER={sql['driver']};
                        SERVER={sql['server']};
                        DATABASE={sql['database']};
                        UID={sql['username']};
                        PWD={sql['password']};
                        TrustServerCertificate=yes;
                    """
    con=pyodbc.connect(connectionstring)
    return con