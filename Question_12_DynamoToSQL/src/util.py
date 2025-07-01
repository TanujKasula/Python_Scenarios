import os 
import configparser
import urllib.parse
import boto3
import urllib
from sqlalchemy import create_engine

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

def get_dynamodb_table():
    config=get_config()
    aws=config['AWS']
    aws_id=aws['aws_access_key_id']
    aws_secret=aws['aws_secret_access_key']
    aws_region=aws['region']
    aws_table=aws['table_name']

    dynamodb=boto3.resource(
        'dynamodb',
        region_name=aws_region,
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret
    )

    table=dynamodb.Table(aws_table)
    return table