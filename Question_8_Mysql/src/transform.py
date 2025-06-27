import pandas as pd

def transform_sales(customers_df,orders_df):
    df=orders_df.groupby('customer_id').agg(
        total_orders=pd.NamedAgg(column='order_id', aggfunc='count'),
        latest_order_date=pd.NamedAgg(column='order_date', aggfunc='max')
    ).reset_index()

    final_df=pd.merge(customers_df,df,on='customer_id',how='inner')
    return final_df