from src.util import get_config,get_s3_client,file_exists
import os

def upload_resume_to_s3():
    s3=get_s3_client()
    config=get_config()
    aws=config['AWS']
    bucket=aws['bucket_name']
    folder1=aws['folder1']
    archive=aws['folder2']
    region=aws['region']

    local_resume_folder=r"C:\Users\Tanuj\Documents\UseCases\Question_15_16_AWS_unstructured\ResumestoUpload"
    for filename in os.listdir(local_resume_folder):
        if filename.endswith(".pdf"):
            file_path=os.path.join(local_resume_folder,filename)
            s3_key=f"{folder1}/{filename}"

            if not file_exists(s3,bucket,s3_key):
                s3.upload_file(file_path,bucket,s3_key)
                print(f"Uploaded {filename} to 's3://{bucket}/{s3_key}' successfully")
            else:
                print(f"File already exists")

# if __name__ =="__main__":
#     upload_resume_to_s3()