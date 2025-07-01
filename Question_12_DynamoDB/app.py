from src.extraction import extract_data
from src.load import load_data

def main():
    print("Initiating data extraction")
    extract_data()
    print("Initiating data loading")
    load_data()

if __name__=="__main__":
    main()