from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
import os
import pickle

SCOPE=['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    token_path=os.path.join(os.path.dirname((os.path.dirname(__file__))),'credentials','token.pickle')
    credentials_path=os.path.join(os.path.dirname((os.path.dirname(__file__))),'credentials','Credentials.json')
    
    creds=None
    if os.path.exists(token_path):
        with open(token_path,'rb') as token:
            creds=pickle.load(token)

    if not creds:
        flow=InstalledAppFlow.from_client_secrets_file(
            credentials_path,SCOPE
        )
        creds=flow.run_local_server(port=0)
        with open(token_path,'wb') as token:
            pickle.dump(creds,token)
    return creds

def authenticate_gmail():
    creds=get_credentials()
    service=build('gmail','v1',credentials=creds)
    return service

authenticate_gmail()