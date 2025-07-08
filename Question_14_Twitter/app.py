from src.Transform import clean_csv
from src.DB_loader import load_db

def main():
    input_file_name="iphone_15.csv"
    output_file_path=clean_csv(input_file_name)
    print("Successfully Transformed")
    load_db("Tweets",output_file_path)
    print("Successfully loaded")

if __name__=="__main__":
    main()
