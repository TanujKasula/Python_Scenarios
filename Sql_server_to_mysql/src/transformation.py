def transform_data(df):
    df=df.loc[df['status']=="active"]
    return df