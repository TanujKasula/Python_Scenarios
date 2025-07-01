import json
import os
from src.util import get_dynamodb_table

def load_data():
    table=get_dynamodb_table()
    json_file=os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','projects.json')
    with open(json_file,'r') as f:
        records=json.load(f)

    for item in records:
        table.put_item(Item=item)

    print("Successfully loaded in to dynamo db")