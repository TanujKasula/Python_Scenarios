from src.util import get_sql_server_engine
import pandas as pd
from sqlalchemy import inspect,text

def load_data(df:pd.DataFrame):
    mode='replace'
    engine=get_sql_server_engine()
    table_name="projects"

    with engine.begin() as conn:
        inspector=inspect(conn)
        table_exists=inspector.has_table(table_name)

        if table_exists:
            result=conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            rows=result.scalar()

            if rows>0:
                mode='append'
    
    df.to_sql(table_name,con=engine,if_exists=mode,index=False)

    print(f"Data loaded to sql server in ({'FULL' if mode=='replace' else 'INCREMENTAL'} mode)")
            