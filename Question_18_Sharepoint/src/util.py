from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from config import config
from sqlalchemy import create_engine
from sqlalchemy import inspect
import urllib

def get_sharepoint_context():
    # ctx=ClientContext(config.sharepoint_url).with_credentials(DeviceCredential())
    # return ctx

    site_url=config.sharepoint_url
    context_auth=AuthenticationContext(site_url)

    context_auth.acquire_token_for_user(config.username,config.password)
    context=ClientContext(site_url,context_auth)
    return context

def get_sql_server_engine():
    connection_string=f"""
                        DRIVER={config.driver};
                        SERVER={config.server};
                        DATABASE={config.database};
                        UID={config.server_username};
                        PWD={config.server_password};
                        TrustServerCertificate=yes;
                    """
    params=urllib.parse.quote_plus(connection_string)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine

def table_exists(engine,table_name):
    inspector=inspect(engine)
    return inspector.has_table(table_name)

