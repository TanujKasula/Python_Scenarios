import pandas as pd
from src.util import sql_server_engine,my_sql_engine

def extract_customers():
    engine=my_sql_engine()
    query="select *from customers"
    df=pd.read_sql(query,engine)
    return df

def extract_orders():
    engine=my_sql_engine()
    query="select * from orders"
    df=pd.read_sql(query,engine)
    return df


# print(extract_customers())
# print(extract_orders())