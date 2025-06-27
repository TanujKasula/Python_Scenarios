import pandas as pd
from sqlalchemy import create_engine
from src.util import get_config
import urllib

def get_sql_server_engine():
    config=get_config()
    sql=config['SQL_SERVER']
    connection_string=f"""
        DRIVER={{{sql['driver']}}};
        SERVER={sql['server']};
        DATABASE={sql['database']};
        UID={sql['username']};
        PWD={sql['password']};
        TrustServerCertificate=yes;
    """
    params=urllib.parse.quote_plus(connection_string)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine

def extract_customers(last_loaded_date=None):
    engine=get_sql_server_engine()
    if last_loaded_date:
        query=f"""
                    select * from cleaned_customers_status
                    where registration_date > '{last_loaded_date}'
                """
    else:
        query="select * from cleaned_customers_status"
    df=pd.read_sql(query,con=engine)
    df.drop(columns=['Country','first_name','last_name'],inplace=True)

    return df

def extract_orders(last_loaded_date=None):
    engine=get_sql_server_engine()
    if(last_loaded_date):
        query=f"""
                    select * from orders
                    where order_date >'{last_loaded_date}'
                """
    else:
        query="select * from orders"
    df=pd.read_sql(query,con=engine)
    return df

