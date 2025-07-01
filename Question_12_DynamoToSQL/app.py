from src.extraction import extract_data
from src.transformation import transform_data
from src.load import load_data

def main():
    df=extract_data()
    transformed_df=transform_data(df)
    load_data(transformed_df)

if __name__=="__main__":
    main()
