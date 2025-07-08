from src.utils import get_sql_server_engine, table_exists
import pandas as pd


def load_db(table_name,transformed_file):
    engine=get_sql_server_engine()
    df=pd.read_csv(transformed_file)
    df.drop(columns=['text'])
    new_order=['cleaned_text','created_at','lang']
    df=df[new_order]
    df.rename({
        "cleaned_text":"Post",
        "created_at":"Posted_date",
        "lang":"Language"
    })
    if table_exists(engine,table_name):
        df.to_sql(table_name,con=engine,index=False,if_exists='append')
    else:
        df.to_sql(table_name,con=engine,index=False,if_exists='replace')