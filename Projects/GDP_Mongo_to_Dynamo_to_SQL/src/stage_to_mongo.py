import os
import json
from util import get_config,get_mongo_client


def get_json_data():
    base_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','gdp_data.json')

    with open(base_path,'r') as f:
        data=json.load(f)

    if isinstance(data,list) and len(data)>1:
        return data[1]
    else:
        raise ValueError("Unexpected Structure of JSON..... Modify the code for it...")
    

def insert_into_mongo(data):
    config=get_config()
    client=get_mongo_client()
    database_name=config['MONGODB']['database']
    collection_name=config['MONGODB']['collection']

    Projects_db=client[database_name]
    GDP_collection=Projects_db[collection_name]

    if GDP_collection.count_documents({})>0:
        GDP_collection.drop()
    
    result=GDP_collection.insert_many(data)
    print(f"Successfully inserted {len(result.inserted_ids)} records into MongoDB Collection '{collection_name}' in database '{database_name}'")


if __name__=="__main__":
    data=get_json_data()
    insert_into_mongo(data)
