import os
from urllib.parse import quote
from src.util import get_config,get_s3_client,file_exists
from datetime import datetime

def generate_s3_folder_path(sender_email,receiver_email,email_date):
    # sender_email = unquote_plus(sender_email)
    # receiver_email = unquote_plus(receiver_email)
    cleaned_receiver = quote(receiver_email, safe='')  # '@' → %40
    cleaned_sender = quote(sender_email, safe='')
    if isinstance(email_date, datetime):
        timestamp = email_date.strftime('%Y-%m-%d_%H-%M-%S')
    else:
        try:
            parsed_date = datetime.strptime(email_date[:25], "%a, %d %b %Y %H:%M:%S")
            timestamp = parsed_date.strftime('%Y-%m-%d_%H-%M-%S')
        except Exception as e:
            print(f"Warning: Failed to parse email_date '{email_date}'. Error: {e}")
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path=f"{cleaned_receiver}/{cleaned_sender}/{timestamp}/"
    return path

def upload_gmail_data(attachments,email_metadata,email_body=None):
    s3=get_s3_client()
    config=get_config()
    aws=config['AWS']
    bucket=aws['bucket_name']
    region=aws['region']

    sender_mail=email_metadata['sender_email']
    receiver_mail=email_metadata['receiver_email']
    email_date=email_metadata['email_date']

    folder_path=generate_s3_folder_path(sender_mail,receiver_mail,email_date)

    attachment_urls=[]
    for attachment in attachments:
        file_name=attachment['filename']
        file_data=attachment['file_data']
        key=f"email_attachments/{folder_path}{file_name}"

        if not file_exists(s3,bucket,key):
            s3.put_object(Bucket=bucket, Key=key, Body=file_data)
        
        url=f"https://{bucket}.s3.{region}.amazonaws.com/{quote(key, safe='')}"
        attachment_urls.append(url)

    email_text_url=None
    if email_body:
        key=f"emails_text/{folder_path}email.txt"
        if not file_exists(s3,bucket,key):
            s3.put_object(Bucket=bucket,Key=key,Body=email_body.encode('utf-8'))
        email_text_url=f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return {
        "folder_url":folder_path,
        "attachment_urls":attachment_urls,
        "email_text_url":email_text_url
    }