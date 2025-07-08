import os 
import configparser
import urllib.parse
import urllib
from sqlalchemy import create_engine
from sqlalchemy import inspect

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.dirname(os.path.dirname(__file__))
    config_path=os.path.join(base_path,'config','config.config')
    config.read(config_path)
    return config

def get_sql_server_engine():
    config=get_config()
    sql=config['SQL_SERVER']
    connection_string=f"""
                        DRIVER={sql['driver']};
                        SERVER={sql['server']};
                        DATABASE={sql['database']};
                        UID={sql['username']};
                        PWD={sql['password']};
                        TrustServerCertificate=yes;
                    """
    params=urllib.parse.quote_plus(connection_string)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine
    
def table_exists(engine,table_name):
    inspector=inspect(engine)
    return inspector.has_table(table_name)