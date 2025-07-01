import os
import json
from src.util import get_config,get_mongo_client

def extract_data():
    config=get_config()
    client=get_mongo_client()
    database=config['MONGODB']['database']
    collection=config['MONGODB']['collection']

    db=client[database]
    table=db[collection]

    docs=list(table.find())

    for doc in docs:
        if '_id' in doc:
            del doc['_id']

    json_file=os.path.join((os.path.dirname(os.path.dirname(__file__))),'data','projects.json')
    with open(json_file,'w') as f:
        json.dump(docs,f,indent=4)
    
    print("JSON extracted frm mongodb")
