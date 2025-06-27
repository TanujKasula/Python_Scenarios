from sqlalchemy import create_engine
from sqlalchemy import inspect
from src.util import get_config
import urllib
import pandas as pd

def get_mysql_engine():
    config=get_config()
    mysql=config['MYSQL']

    encoded_password=urllib.parse.quote_plus(mysql['password'])
    ConnectionString=f"mysql+mysqlconnector://{mysql['user']}:{encoded_password}@{mysql['host']}:{mysql['port']}/{mysql['database']}"
    engine=create_engine(ConnectionString)
    return engine

def table_exists(engine,table_name):
    inspector=inspect(engine)
    return inspector.has_table(table_name)


def load_customers(df):
    engine=get_mysql_engine()
    if table_exists(engine,"customers"):
        with engine.begin() as con:
            existing_ids=pd.read_sql("select customer_id from customers",con)
            df=df[~df['customer_id'].isin(existing_ids['customer_id'])]
            df.to_sql('customers',con=engine,if_exists='append',index=False)
    else:
        df.to_sql('customers',con=engine,if_exists='replace',index=False)

def load_orders(df):
    engine=get_mysql_engine()
    if table_exists(engine,"orders"):
        with engine.begin() as con:
            existing_ids=pd.read_sql("select order_id from orders",con)
            df=df[~df['order_id'].isin(existing_ids['order_id'])]
            if df.empty:
                print("orders are empty")
            else:
                df.to_sql('orders',con=engine,if_exists='append',index=False)
    else:
        if df.empty:
            print("Order DataFrame is empty. Nothing to load.")
            return
        df.to_sql('orders', con=engine, if_exists='replace', index=False)