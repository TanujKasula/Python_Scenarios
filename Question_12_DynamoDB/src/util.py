import configparser
import os
from pymongo import MongoClient
import boto3

def get_config():
    config=configparser.ConfigParser()
    base_path=os.path.dirname(os.path.dirname(__file__))
    config_path=os.path.join(base_path,'config','config.config')
    config.read(config_path)
    return config

def get_mongo_client():
    config=get_config()
    host=config['MONGODB']['host']
    port=int(config['MONGODB']['port'])
    client=MongoClient(host,port)
    return client

def get_dynamodb_table():
    config=get_config()
    aws_config=config['AWS']
    aws_id=aws_config['aws_access_key_id']
    aws_secret=aws_config['aws_secret_access_key']
    aws_region=aws_config['region']
    aws_table=aws_config['table_name']

    dynamodb=boto3.resource(
        'dynamodb',
        region_name=aws_region,
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret
    )
    return dynamodb.Table(aws_table)
