import os
import configparser
import boto3
from sqlalchemy import create_engine
from pymongo import MongoClient
import urllib

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'config','config.config')
    config.read(base_path)
    return config


def get_mongo_client():
    config=get_config()
    host=config['MONGODB']['host']
    port=int(config['MONGODB']['port'])
    client=MongoClient(host,port)
    return client


def get_dynamodb_client():
    config=get_config()
    aws=config['AWS']
    access_id=aws['aws_access_key_id']
    secret_key=aws['aws_secret_access_key']
    region=aws['region']
    client=boto3.client(
        'dynamodb',
        aws_access_key_id=access_id,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    return client


def get_dynamodb_resource():
    config=get_config()
    aws=config['AWS']
    access_id=aws['aws_access_key_id']
    secret_key=aws['aws_secret_access_key']
    region=aws['region']
    client=boto3.resource(
        'dynamodb',
        aws_access_key_id=access_id,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    return client


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

def get_mysql_engine():
    config=get_config()
    mysql=config['MYSQL']
    encodedpassword=urllib.parse.quote_plus(mysql['password'])
    connectionString=f"mysql+mysqlconnector://{mysql['user']}:{encodedpassword}@{mysql['host']}:{mysql['port']}/{mysql['database']}"
    return create_engine(connectionString)
