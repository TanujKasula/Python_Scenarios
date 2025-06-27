import pandas as pd
from src.util import get_sqlserver_engine
from sqlalchemy import text

def scd2_load(insert_df,expire_df):
    engine=get_sqlserver_engine()

    with engine.begin() as con:
        for _,row in expire_df.iterrows():
            con.execute(text("""
                              update scd_customer_dim
                              set is_current=0,
                              valid_to=:valid_to
                              where customer_id=:customer_id and is_current=1
                              """),{
                                  "valid_to":row['valid_to'],
                                  "customer_id":row['customer_id']
                              })
            
        insert_df.to_sql('scd_customer_dim',con,if_exists='append',index=False)

        if not insert_df.empty:
            max_date=insert_df['valid_from'].max()
            con.execute(text("""
                    MERGE metadata as target
                    using (select :table_name as table_name,:last_loaded_date as last_loaded_date) as source
                    on target.table_name=source.table_name
                    when matched then
                             update set last_loaded_date=source.last_loaded_date
                    when not matched then
                             insert (table_name,last_loaded_date) values(source.table_name,source.last_loaded_date);
                    """),{
                        "table_name":"scd_customer_dim",
                        "last_loaded_date":max_date
                    })
    print("Loading completed")