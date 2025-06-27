import pandas as pd
from sqlalchemy import text
from src.util import get_sqlserver_engine


def get_existing_records(table_name):
    engine=get_sqlserver_engine()
    query=f"select * from {table_name} where is_current= 1 "
    return pd.read_sql(query,engine)

def prepare_scd2_data(incoming_df):
    engine=get_sqlserver_engine()
    today=pd.to_datetime("now").normalize()

    current_df=get_existing_records("scd_customer_dim")
    incoming_df=incoming_df.sort_values(['customer_id','last_updated'])

    rows_to_insert=[]
    rows_to_expire=[]

    for customer_id,group in incoming_df.groupby('customer_id'):
        customer_versions=group.reset_index(drop=True)

        #this current record is the corresponding customer record for this loop i
        current_record=current_df[current_df['customer_id']==customer_id]
        previous_version=current_record.iloc[0].to_dict() if not current_record.empty else None

        for index,row in customer_versions.iterrows():
            new_version=row.to_dict()
            compare_fields=['full_name', 'email_address', 'current_city',
                              'preferred_language', 'subscription_status', 'last_purchase_date']
            
            is_changed=(
                previous_version is None or
                any(previous_version.get(col) != new_version.get(col) for col in compare_fields)
            )

            if is_changed:
                if previous_version:
                    # expose old row
                    rows_to_expire.append({
                        'customer_id':previous_version['customer_id'],
                        'valid_to':pd.to_datetime(new_version['last_updated'])-pd.Timedelta(seconds=1)
                    })

                    # insert new row
                rows_to_insert.append({
                        'customer_id':new_version['customer_id'],
                        'full_name': new_version['full_name'],
                        'email_address': new_version['email_address'],
                        'current_city': new_version['current_city'],
                        'preferred_language': new_version['preferred_language'],
                        'subscription_status': new_version['subscription_status'],
                        'last_purchase_date': new_version['last_purchase_date'],
                        'valid_from': new_version['last_updated'],
                        'valid_to': None,
                        'is_current': 1
                })
                previous_version=new_version
    insert_df=pd.DataFrame(rows_to_insert)
    expire_df=pd.DataFrame(rows_to_expire)

    print("Prepared new versions and expired version")
    return insert_df,expire_df