import urllib
import pandas as pd
from sqlalchemy import create_engine
from src.utils import get_config

def extract_data():
    config=get_config()
    sql=config['SQL_SERVER']
    connectionstring=f"""
        DRIVER={{{sql['driver']}}};
        SERVER={sql['server']};
        DATABASE={sql['database']};
        UID={sql['username']};
        PWD={sql['password']};
        TrustServerCertificate=yes;
    """
    params=urllib.parse.quote_plus(connectionstring)
    engine=create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    customer_df=pd.read_sql('select * from sales.customers',con=engine)
    return customer_df