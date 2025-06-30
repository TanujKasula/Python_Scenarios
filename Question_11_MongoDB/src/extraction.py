import pandas as pd
from src.utils import get_config,get_mongo_client

def extract_from_mongo():
    client=get_mongo_client()
    config=get_config()

    db_name=config['MONGODB']['database']
    collection_name=config['MONGODB']['collection']

    db=client[db_name]
    collection=db[collection_name]

    docs=list(collection.find())

    df=pd.DataFrame(docs)

    if '_id' in df.columns:
        df.drop(columns=['_id'],inplace=True)

    print("Documents fetched successfuly")
    return df

if __name__ == "__main__":
    df = extract_from_mongo()
    print(df.head())

