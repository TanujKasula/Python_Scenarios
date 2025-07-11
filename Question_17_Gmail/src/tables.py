from src.util import get_sql_server_engine
from sqlalchemy import text
def create_tables():
    engine=get_sql_server_engine()

    with engine.begin() as conn:

        schemas="""
                    if not exists(select * from sys.schemas where name='gmail')
                    begin
                        exec('create schema gmail');
                    end
                """
        
        conn.execute(text(schemas))

        query1="""
                    IF NOT EXISTS(SELECT * FROM sysobjects where name='Email_communications' and xtype='U')
                    create table gmail.Email_communications(
                        id int primary key identity(1,1),
                        sender_name nvarchar(255),
                        sender_email nvarchar (255),
                        receiver_email nvarchar(255),
                        receiver_name nvarchar(255),
                        cc nvarchar(max),
                        subject nvarchar(max),
                        body nvarchar(max),
                        email_date DATETIME,
                        folder_url nvarchar(600),
                        email_text_url nvarchar(600)
                    );
                """
        
        conn.execute(text(query1))

        query2="""
                    IF NOT EXISTS(SELECT * FROM sysobjects where name='Email_Attachments' and xtype='U')
                    create table gmail.Email_Attachments(
                        id int primary key identity(1,1),
                        folder_url nvarchar(600),
                        sender_email nvarchar (255),
                        attachment_url nvarchar(1000)
                    );
                """
        conn.execute(text(query2))

        query3="""
                    IF NOT EXISTS(SELECT * FROM sysobjects where name='Email_communications_flat' and xtype='U')
                    create table gmail.Email_communications_flat(
                        id int primary key identity(1,1),
                        sender_name nvarchar(255),
                        sender_email nvarchar (255),
                        receiver_email nvarchar(255),
                        receiver_name nvarchar(255),
                        cc nvarchar(max),
                        subject nvarchar(max),
                        body nvarchar(max),
                        email_date DATETIME,
                        email_text_url nvarchar(600),
                        attachment_1_url nvarchar(1000),
                        attachment_2_url nvarchar(1000),
                        attachment_3_url nvarchar(1000),
                        attachment_4_url nvarchar(1000)
                    );
                """
        conn.execute(text(query3))

        print("Schema gmail and tables are created successfully (or already exists)")

if __name__=="__main__":
    create_tables()