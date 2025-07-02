from src.util import get_config,get_dynamodb_client,get_dynamodb_resource
import pandas as pd

def extract_data():
    resource=get_dynamodb_resource()
    config=get_config()
    table_name=config['AWS']['table_name']
    dynamo_table=resource.Table(table_name)

    items=[]
    response=dynamo_table.scan()

    items.extend(response.get('Items',[]))

    while 'LastEvaluatedKey' in response:
        response=dynamo_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items',[]))

    print("Successfully extracted from DynamoDB table")
    df=pd.DataFrame(items)
    return df

# if __name__=="__main__":
#     df=extract_data()
#     print(df)
