from src.util import get_sql_server_engine,table_exists
def load(df,table_name,if_exist):
    engine=get_sql_server_engine()
    df.to_sql(name=table_name,con=engine,index=False,if_exists=if_exist)
    print("Data loaded Successfully")