import pandas as pd
from src.extract import extract_orders,extract_customers
from src.transform import transform_sales
from src.load import load_summary

def main():
    print(" Starting ETL Process for Customer Sales Summary...")

    # Step 1: Extract
    print("Extracting orders from MySQL...")
    orders_df = extract_orders()
    customers_df = extract_customers()

    if orders_df.empty:
        print(" No orders found. ETL stopped.")
        return

    # Step 2: Transform
    print("Transforming data: Aggregating customer sales...")
    summary_df = transform_sales(customers_df,orders_df)

    # Step 3: Load
    print("Loading aggregated data to SQL Server...")
    load_summary(summary_df)

    print(" ETL Process Completed Successfully!")

if __name__ == "__main__":
    main()
