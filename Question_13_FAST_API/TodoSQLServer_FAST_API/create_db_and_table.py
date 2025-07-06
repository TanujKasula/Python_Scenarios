from util import get_config
import pyodbc

def create_db(db_name):
    try:
        config=get_config()
        sql=config["SQL_SERVER"]
        connectionstring=f"""
                            DRIVER={sql['driver']};
                            SERVER={sql['server']};
                            DATABASE=Bikestores;
                            UID={sql['username']};
                            PWD={sql['password']};
                            TrustServerCertificate=yes;
                        """
        master_con=pyodbc.connect(connectionstring,autocommit=True)
        master_cursor=master_con.cursor()
        master_cursor.execute(f"IF DB_ID('{db_name}') IS NULL CREATE DATABASE {db_name}")

        master_con.commit()
        print(f"Database {db_name} created or already exists")

    except Exception as e:
        print("Error creating a database",e)

def create_table(table_name,db_name):
    try:
        config=get_config()
        sql=config["SQL_SERVER"]
        connectionstring=f"""
                            DRIVER={sql['driver']};
                            SERVER={sql['server']};
                            DATABASE={db_name};
                            UID={sql['username']};
                            PWD={sql['password']};
                            TrustServerCertificate=yes;
                        """
        con=pyodbc.connect(connectionstring)
        cursor=con.cursor()
        cursor.execute(f"""
                            IF OBJECT_ID('{table_name}','U') IS NULL
                            CREATE TABLE {table_name}(
                                id INT IDENTITY(1,1) PRIMARY KEY,
                                title NVARCHAR(255) NOT NULL,
                                description NVARCHAR(max) ,
                                completed BIT DEFAULT 0
                            )
                        """)
        con.commit()
        print(f"Table {table_name} created or already exists")

    except Exception as e :
        print("Error occured while while creating table",e)

if __name__=="__main__":
    create_db("API")
    create_table("todos","API")