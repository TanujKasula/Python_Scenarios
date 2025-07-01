import pandas as pd

def transform_data(df):
    df['start_date']=pd.to_datetime(df['start_date'])
    df['end_date']=pd.to_datetime(df['end_date'])

    new_order=['project_id','project_name', 'client','domain','location','technologies', 'project_manager',
                 'start_date', 'end_date','status' ]
    
    for col in new_order:
        if col not in df.columns:
            df[col]=pd.NA

    df=df[new_order]
    if 'technologies' in df.columns:
        df['technologies']=df['technologies'].apply(lambda x:', '.join(x) if isinstance(x,list) else x)

    print("Transformation completed")
    return df