from src.extract import extract_all_json_files
from src.transform import transform_all
from src.load import load_to_sql

def main():
    dfs=extract_all_json_files()
    transformed_dfs=transform_all(dfs)
    # for name,df in transformed_dfs.items():
    #     print(f"___{name}___")
    #     print(df.head())
    load_to_sql(transformed_dfs)

if __name__=="__main__":
    main()