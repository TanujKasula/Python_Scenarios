import pandas as pd
from src.extract import extract_customers,extract_orders
from src.transform import transform_customers,transform_orders
from src.load import load_customers,load_orders
from src.util import read_last_loaded_date,update_last_loaded_date


def main():
    print("Starting ETL Process......")

    print("Starting Extraction of Customers")
    cust_last_date=read_last_loaded_date("customers")
    customer_df=extract_customers(last_loaded_date=cust_last_date)
    
    if not customer_df.empty:
        print("Starting Transformations of customers")
        customer_df=transform_customers(customer_df)
        print("Starting Loading of customers")
        load_customers(customer_df)
        print("Customers loaded successfully")
        max_date=pd.to_datetime(customer_df['registration_date']).max()
        update_last_loaded_date("customers",max_date)
    else:
        print("No new customers to load")

    print("Processing Orders.Please Wait....")

    print("Extracting orders.....")
    orders_last_date=read_last_loaded_date("orders")
    orders_df=extract_orders(orders_last_date)

    if not orders_df.empty:
        print("Transforming orders.....")
        print("Loading Orders.....")
        load_orders(orders_df)
        print("Orders Processed successfully")
        max_date=pd.to_datetime(orders_df['order_date']).max()
        update_last_loaded_date("orders",max_date)
    else:
        print("No orders to process")
    print("Completed ETL successfully")


if __name__=="__main__":
    main()