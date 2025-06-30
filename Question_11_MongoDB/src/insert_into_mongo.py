import os
import json
from src.utils import get_mongo_client,get_mysql_engine,get_sqlserver_engine,get_config

def insert_data_into_mongo():
    base_path=os.path.dirname(__file__)
    txt_file=os.path.join(base_path,'..','data','Doc_unstructured_1.txt')

    with open(txt_file,'r') as f:
        raw_txt=f.read()

    data=json.loads(raw_txt)
    client=get_mongo_client()
    config=get_config()

    db_name=config['MONGODB']['database']
    collection_name=config['MONGODB']['collection']

    db=client[db_name]
    collection=db[collection_name]

    collection.delete_many({})
    collection.insert_many(data)

if __name__ == "__main__":
    insert_data_into_mongo()