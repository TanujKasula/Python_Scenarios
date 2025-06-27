from src.util import get_sqlserver_engine,get_mysql_engine
import pandas as pd
from sqlalchemy import text

def get_last_loaded_date(table_name='scd_customer_dim'):
    engine=get_sqlserver_engine()
    with engine.begin() as con:
        result=con.execute(text("select last_loaded_date from metadata where table_name=:table"),{"table":table_name}).fetchone()
        return result[0] if result else None
    
def extract_customer_data():
    mysql_engine=get_mysql_engine()
    last_loaded_date=get_last_loaded_date()
    query="select * from customer_dim"
    if last_loaded_date:
        query=query+ f" where last_updated > '{last_loaded_date}'"
    df=pd.read_sql(query,con=mysql_engine)

    print("Successfully extracted data from source table")
    return df