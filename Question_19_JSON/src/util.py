import os
from dotenv import load_dotenv
from getpass import getpass
import urllib
from sqlalchemy import create_engine
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from src.config import driver,server,server_password,server_username,database
def get_sharepoint_context():
    load_dotenv()
    sharepoint_password=getpass("Enter your sharepoint password:")
    folder_path = os.getenv("SHAREPOINT_FOLDER_PATH")
    context_auth=AuthenticationContext(os.getenv("SHAREPOINT_URL"))
    context_auth.acquire_token_for_user(os.getenv("SHAREPOINT_USERNAME"),sharepoint_password)
    context=ClientContext(os.getenv("SHAREPOINT_URL"),context_auth)
    return context,folder_path

def get_sql_server_engine():
    connection_string=f"""
                        DRIVER={driver};
                        SERVER={server};
                        DATABASE={database};
                        UID={server_username};
                        PWD={server_password};
                        TrustServerCertificate=yes;
                    """
    params=urllib.parse.quote_plus(connection_string)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine