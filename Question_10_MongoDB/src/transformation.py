from src.utils import get_sql_engine
from src.extraction import extract_from_mongodb
import pandas as pd

def transform_data(df):
    df['technologies']=df['technologies'].apply(lambda x:','.join(x))
    df['_id'] = df['_id'].astype(str)
    return df

# if __name__=="__main__":
#     df=extract_from_mongodb("projects")
#     transformed_df=transform_data(df)
#     print(transformed_df['technologies'])