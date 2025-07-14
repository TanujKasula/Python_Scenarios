from src.extract import extract
from src.transform import transform
from src.load import load
from src.util import table_exists,get_sql_server_engine
from config import config

def main():
    table_name=config.table
    df=extract()
    transformed_df=transform(df)
    if_exist='replace'
    load(transformed_df,table_name,if_exist)
    print("Closing pipeline...")

if __name__=="__main__":
    main()