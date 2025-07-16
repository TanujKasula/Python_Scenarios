import pandas as pd
from src.util import get_sql_server_engine
from sqlalchemy import text

def apply_constraints(engine):
    with engine.begin() as conn:
        print(f"Applying constraints....")

        constraints=[
            "ALTER TABLE product_dimension ALTER COLUMN product_id INT NOT NULL;",
            "ALTER TABLE store_dimension ALTER COLUMN store_id INT NOT NULL;",
            "ALTER TABLE time_dimension ALTER COLUMN date_id INT NOT NULL;",
            "ALTER TABLE supplier_dimension ALTER COLUMN supplier_id INT NOT NULL;",
            "ALTER TABLE promotion_dimension ALTER COLUMN promotion_id INT NOT NULL;",
            "ALTER TABLE sales_fact ALTER COLUMN sale_id INT NOT NULL;",

            "ALTER TABLE product_dimension ADD primary key (product_id);",
            "ALTER TABLE store_dimension ADD primary key (store_id);",
            "ALTER TABLE time_dimension ADD primary key (date_id);",
            "ALTER TABLE supplier_dimension ADD primary key (supplier_id);",
            "ALTER TABLE promotion_dimension ADD primary key (promotion_id);",
            "ALTER TABLE sales_fact ADD primary key (sale_id);",

            "ALTER TABLE sales_fact ADD FOREIGN KEY(product_id) REFERENCES product_dimension(product_id);",
            "ALTER TABLE sales_fact ADD FOREIGN KEY(store_id) REFERENCES store_dimension(store_id);",
            "ALTER TABLE sales_fact ADD FOREIGN KEY(date_id) REFERENCES time_dimension(date_id);",
            "ALTER TABLE sales_fact ADD FOREIGN KEY(supplier_id) REFERENCES supplier_dimension(supplier_id);",
            "ALTER TABLE sales_fact ADD FOREIGN KEY(promotion_id) REFERENCES promotion_dimension(promotion_id);",
        ]
        for query in constraints:
            try:
                conn.execute(text(query))
            except:
                print(f"Failed {query.strip()}")

def load_to_sql(dataframes:dict):
    engine=get_sql_server_engine()
    for table_name,df in dataframes.items():
        print(f"Loading {table_name}....")
        df.to_sql(table_name,con=engine,index=False,if_exists='replace')
        print(f"{table_name} loaded successfuly!!!")
    print("All tables loaded successfully")
    apply_constraints(engine)