from src.util import get_dynamodb_table
import pandas as pd

def extract_data():
    table=get_dynamodb_table()
    items=[]
    response=table.scan()
    items.extend(response.get('Items',[]))

    while 'LastEvaluatedKey' in response:
        response=table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items',[]))

    print("Successfully Extracted from the dynamodb table")
    df=pd.DataFrame(items)
    return df

if __name__=="__main__":
    df=extract_data()
    print(df.columns)