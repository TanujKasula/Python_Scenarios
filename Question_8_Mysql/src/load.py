import pandas as pd
from sqlalchemy import inspect
from src.util import sql_server_engine

def table_exists(table_name,engine):
    inspector=inspect(engine)
    return inspector.has_table(table_name)

def load_summary(df):
    engine=sql_server_engine()
    
    if table_exists('customers_sales_summary',engine):
        df.to_sql('customers_sales_summary',con=engine,index=False,if_exists='append')
    else:
        df.to_sql('customers_sales_summary',con=engine,index=False,if_exists='replace')