from src.extraction import extract_from_mongodb
from src.transformation import transform_data
from src.load import load_data_to_sql

def main():
    df=extract_from_mongodb("projects")
    print("Successfully extracted")
    transform_df=transform_data(df)
    print("Data transformed successfully")
    load_data_to_sql(df)

if __name__=="__main__":
    main()