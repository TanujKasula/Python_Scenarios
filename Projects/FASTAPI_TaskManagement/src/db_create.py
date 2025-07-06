from src.util import get_db_connection

def create_tables():
    connection=get_db_connection()
    cursor=connection.cursor()
    user_query="""
                IF NOT EXISTS(SELECT * FROM sysobjects WHERE name='users' and xtype='U')
                CREATE TABLE users(
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name NVARCHAR(100) NOT NULL,
                    email NVARCHAR(100) UNIQUE NOT NULL,
                    password NVARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT GETDATE()
                )
          """
    cursor.execute(user_query)

    tasks_query="""
                    IF NOT EXISTS(select * from sysobjects where name='tasks' and xtype='U')
                    CREATE TABLE tasks(
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            title NVARCHAR(100) NOT NULL,
                            description NVARCHAR(MAX),
                            status NVARCHAR(50) DEFAULT 'Pending',
                            due_date DATE,
                            user_id INT FOREIGN KEY REFERENCES users(id)
                    )
                
                """
    cursor.execute(tasks_query)

    connection.commit()
    cursor.close()
    connection.close()
