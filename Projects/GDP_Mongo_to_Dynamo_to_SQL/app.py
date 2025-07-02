from src.extract_from_dynamo  import extract_data
from src.transform import transform_data
from src.dynamo_to_mysql import load_to_mysql
from src.dynamo_to_sqlserver import load_to_sql_server

def main():
    df=extract_data()
    transform_df=transform_data(df)
    print("Start loading process.....")
    load_to_mysql(transform_df,"GDP")
    load_to_sql_server(transform_df,"GDP")
    print("The ETL is done successfully!!!!!!!")

    
if __name__=="__main__":
    main()
