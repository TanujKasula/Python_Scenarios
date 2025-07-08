import os
from botocore.exceptions import ClientError
from tempfile import gettempdir

from src.resume_parser import parse_resume
from src.transform import transform_parsed_data
from src.db_insert import insert_resume_data
from src.util import get_config,get_s3_client

def process_resumes_from_s3():
    config=get_config()
    aws=config['AWS']
    bucket_name=aws['bucket_name']
    resume_folder=aws['folder1']
    archive_folder=aws['folder2']
    region=aws['region']
    
    s3=get_s3_client()

    try:
        response=s3.list_objects_v2(Bucket=bucket_name,Prefix=f"{resume_folder}/")
        if 'Contents' not in response:
            print("No resumes found in s3")
            return 
        for obj in response['Contents']:
            key=obj['Key']
            if key.endswith('/'):
                continue

            filename=os.path.basename(key)
            print(f"Processing '{filename}'......")
            localpath=os.path.join(gettempdir(),filename)
            s3.download_file(bucket_name,key,localpath)

            parsed_data=parse_resume(localpath)
            transformed_data=transform_parsed_data(parsed_data)
            insert_resume_data(transformed_data)

            archive_key=key.replace(f"{resume_folder}/",f"{archive_folder}/")
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket':bucket_name,'Key':key},
                Key=archive_key
            )
            s3.delete_object(Bucket=bucket_name, Key=key)
            print(f"File '{filename}' archived to :'{archive_key}' ")

    except ClientError as e:
        print("AWS Error Occured")