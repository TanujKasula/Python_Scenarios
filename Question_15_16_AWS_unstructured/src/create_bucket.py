import boto3
from src.util import get_config,file_exists
from botocore.exceptions import ClientError
from src.util import get_s3_client

def create_bucket_and_folders():
    config=get_config()
    aws=config['AWS']
    bucket_name=aws['bucket_name']
    folder1=aws['folder1']
    folder2=aws['folder2']
    region=aws['region']
    
    s3=get_s3_client()
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint':region}
        )
        print(f"Bucket {bucket_name} created successfully")
    except ClientError as e:
        if e.response['Error']['Code']=='BucketAlreadyOwnedByYou':
            print(f"Bucket {bucket_name} already exists")
        else:
            print("Error is :",e)
    
    for folder in [f"{folder1}/",f"{folder2}/"]:
        if not file_exists(s3,bucket_name,folder):
            s3.put_object(Bucket=bucket_name,Key=folder)
            print(f"Folder '{folder}' created inside the bucket '{bucket_name}'")
        else:
            print(f"Folder '{folder}' already exists")

if __name__=="__main__":
    create_bucket_and_folders()