import os
import json
from utils import get_config,get_mongo_client

txt_path=os.path.join(os.path.dirname(__file__),'..','data','project.txt')
with open(txt_path,'r') as f:
    text_data=f.read()

json_data=json.loads(text_data)

client=get_mongo_client()
db=client['pythonetl']
project=db['projects']

project.insert_many(json_data)

for doc in project.find():
    print(doc)