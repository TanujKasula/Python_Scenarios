def transform_customers(df):
    if 'registration_date' in df.columns:
        df=df.sort_values(by='registration_date')
    return df

def transform_orders(df):
    if'order_date' in df.columns:
        df=df.sort_values(by='order_date')