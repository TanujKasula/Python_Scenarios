from src.load import load_data
from src.extraction import extract_data
from src.transformation import transform_data

def main():
    df=extract_data()
    print("Data extracted:")
    print(df)
    df=transform_data(df)
    print("Data Transformed")
    load_data(df)
    print('Data loaded')

if __name__=="__main__":
    main()
