from util import get_config,get_dynamodb_client,get_mongo_client,get_dynamodb_resource
from decimal import Decimal

def get_data_from_mongo():
    client=get_mongo_client()
    config=get_config()
    database_name=config['MONGODB']['database']
    collection_name=config['MONGODB']['collection']

    Projects_db=client[database_name]
    GDP_collection=Projects_db[collection_name]

    return list(GDP_collection.find({},{'_id':0}))


def create_dynamo_table_if_not_exists(dynamo,table_name):
    existing_tables=[table.name for table in dynamo.tables.all()]
    if table_name not in existing_tables:
        table=dynamo.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName':'country_code','KeyType':'HASH'},
                {'AttributeName':'year','KeyType':'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName':'country_code','AttributeType':'S'},
                {'AttributeName':'year','AttributeType':'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"Creating DynamoDB table '{table_name}' .......")
        table.wait_until_exists()
        print(f"Created table '{table_name}' successfully!!!!")
    else:
        print("Table Already Exists!!!")

def insert_into_dynamo_db(dynamo,table_name,data):
    table=dynamo.Table(table_name)
    with table.batch_writer() as batch:
        for row in data:
            batch.put_item({
                'country_code':row.get('countryiso3code','UNKNOWN'),
                'country':row.get('country',{}).get('value','UNKNOWN'),
                'year':row.get('date','0000'),
                'gdp':Decimal(str(row['value'])) if row.get('value') else 0.0
            })
    print(f"Successfully Inserted {len(data)} records into table '{table_name}'.")

def run():
    dynamo=get_dynamodb_resource()
    config=get_config()
    table_name=config['AWS']['table_name']
    data=get_data_from_mongo()
    create_dynamo_table_if_not_exists(dynamo,table_name)
    insert_into_dynamo_db(dynamo,table_name,data)


if __name__=="__main__":
    run()