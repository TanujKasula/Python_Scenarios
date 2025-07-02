import pandas as pd
from src.extract_from_dynamo import extract_data
def calc_cagr(start_val,end_val,period):
    if start_val==0 or period==0 :
        return 0.0
    return ((end_val/start_val)**(1/period))-1

def transform_data(df):
    df['year']=df['year'].astype(int)
    df['gdp']=df['gdp'].astype(float)

    df=df.sort_values(by='year').reset_index(drop=True)

    df['gdp_yoy_growth_%']=df['gdp'].pct_change().fillna(0) * 100
    df['gdp_diff_from_prev_year']=df['gdp'].diff().fillna(0)
    df['gdp_rank']=df['gdp'].rank(ascending=False).astype(int)

    start_year=df['year'].iloc[0]
    start_value=df['gdp'].iloc[0]

    df['cagr_from_start']=df.apply(
        lambda x:calc_cagr(start_value,x['gdp'],x['year']-start_year) if x['year']>start_year else 0.0,
        axis=1
    )

    new_order=['country_code','country','year','gdp','gdp_rank','gdp_yoy_growth_%','gdp_diff_from_prev_year','cagr_from_start']
    for col in df.columns:
        if col not in new_order:
            df[col]=pd.NA
        
    df=df[new_order]

    print("Transformation completed.")
    return df

# if __name__=="__main__":
#     extracted_df=extract_data()
#     df_transformed=transform_data(extracted_df)
#     print(df_transformed)