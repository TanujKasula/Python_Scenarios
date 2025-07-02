import pandas as pd
from src.util import get_config,get_mysql_engine
from src.extract_from_dynamo import extract_data
from src.transform import transform_data
import sqlalchemy

def load_to_mysql(df,table_name):
    engine=get_mysql_engine()

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',
        index=False,
        dtype={
            'country_code':sqlalchemy.types.NVARCHAR(length=10),
            'country': sqlalchemy.types.NVARCHAR(length=50),
            'year': sqlalchemy.types.INTEGER(),
            'gdp': sqlalchemy.types.FLOAT(),
            'gdp_rank': sqlalchemy.types.INTEGER(),
            'gdp_yoy_growth_%': sqlalchemy.types.FLOAT(),
            'gdp_diff_from_prev_year': sqlalchemy.types.FLOAT(),
            'cagr_from_start': sqlalchemy.types.FLOAT()
        }
    )

    print("Successfully loaded to MySQL")