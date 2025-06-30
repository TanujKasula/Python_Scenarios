import pandas as pd
from src.utils import get_config,get_mongo_client

def extract_from_mongodb(collection):
    config=get_config()
    client=get_mongo_client()
    database=config['MONGODB']['database']
    db=client[database]
    table=db[collection]
    data=list(table.find())
    df=pd.DataFrame(data)

    return df

if __name__=="__main__":
    table=extract_from_mongodb("projects")
    print(table.head())
