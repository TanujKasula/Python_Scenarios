import pandas as pd

def transform(df):
    print("Transformin....")
    # df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")

    df['start_date']=pd.to_datetime(df['start_date'],errors='coerce')
    df['end_date']=pd.to_datetime(df['end_date'],errors='coerce')

    df['budget']=pd.to_numeric(df['budget'],errors='coerce')
    return df