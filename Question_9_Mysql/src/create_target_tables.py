from sqlalchemy import text
from util import get_sqlserver_engine

def setup_target_tables():
    engine=get_sqlserver_engine()

    create_scd_table="""
                    if object_id('scd_customer_dim') is null
                    create table scd_customer_dim(
                        surrogate_key INT IDENTITY(1,1) PRIMARY KEY,
                        customer_id INT,
                        full_name VARCHAR(100),
                        email_address VARCHAR(100),
                        current_city VARCHAR(50),
                        preferred_language VARCHAR(30),
                        subscription_status VARCHAR(30),
                        last_purchase_date DATE,
                        valid_from DATETIME,
                        valid_to DATETIME,
                        is_current BIT
                    );
                """
    create_metadata_table="""
                                if object_id('metadata') is null
                                create table metadata(
                                    table_name varchar(50) primary key,
                                    last_loaded_date datetime
                                )
                            """
    with engine.begin() as con:
        con.execute(text(create_scd_table))
        con.execute(text(create_metadata_table))

    print("Tables created")

if __name__=="__main__":
    setup_target_tables()