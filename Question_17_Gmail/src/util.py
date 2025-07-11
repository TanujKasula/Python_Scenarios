import os 
from configparser import ConfigParser
import urllib
from sqlalchemy import create_engine
import boto3


def get_config():
    config=ConfigParser()
    base_dir=os.path.dirname(os.path.dirname(__file__))
    config_path=os.path.join(base_dir,"config","config.config")
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

def get_s3_client():
    config=get_config()
    aws=config['AWS']
    bucket_name=aws['bucket_name']
    region=aws['region']

    s3=boto3.client('s3',region_name=region)
    return s3

def file_exists(s3,bucket_name,key):
    try:
        s3.head_object(Bucket=bucket_name,Key=key)
        return True
    except:
        return False