from src.utils import get_sql_engine
import pandas as pd

def load_data_to_sql(df):
    engine=get_sql_engine()
    df.to_sql('projects',con=engine,index=False,if_exists='replace')
    print("Data is successfully loaded")