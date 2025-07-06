import os
import configparser
import hashlib
import pyodbc

def get_config():
    base_path=os.path.dirname(os.path.dirname(__file__))
    config_path=os.path.join(base_path,'config','config.config')
    config=configparser.ConfigParser()
    config.read(config_path)
    return config

def get_db_connection():
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

def hash_password(password:str) -> str:
    hashed_pwd=hashlib.sha256(password.encode()).hexdigest()
    return hashed_pwd
