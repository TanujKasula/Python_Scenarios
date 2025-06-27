from src.extract import extract_customer_data
from src.transform import prepare_scd2_data
from src.load import scd2_load

def main():
    print("Starting SCD Type 2 ETL Process")

    # Step 1: Extract data from MySQL
    incoming_df = extract_customer_data()
    if incoming_df.empty:
        print("No new or updated data found. Exiting ETL.")
        return

    # Step 2: Transform into new and expired SCD Type 2 records
    insert_df, expire_df = prepare_scd2_data(incoming_df)

    # Step 3: Load the transformed data into SQL Server
    scd2_load(insert_df, expire_df)

    print("ETL process completed successfully.")

if __name__ == "__main__":
    main()
