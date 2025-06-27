import pandas as pd
from sqlalchemy import text
from util import get_mysql_engine

def insert_sample_data():
    engine=get_mysql_engine()

    create_stmt="""
                    create table if not exists customer_dim(
                        customer_id INT PRIMARY KEY,
                        full_name VARCHAR(100),
                        email_address VARCHAR(100),
                        current_city VARCHAR(50),
                        preferred_language VARCHAR(30),
                        subscription_status VARCHAR(30),
                        last_purchase_date DATE,
                        last_updated DATETIME
                    )                
                """
    data=[
        (101, 'Tanuj Kasula', 'tanuj@rare.in', 'Hyderabad', 'Telugu', 'Premium', '2024-12-30', '2025-06-25 10:00:00'),
        (102, 'Meenu Bansal', 'meenu@bmail.com', 'Delhi', 'Hindi', 'Free', '2025-01-10', '2025-06-25 10:10:00'),
        (103, 'Smruthi Rao', 'smruthi@rediffmail.com', 'Bengaluru', 'Kannada', 'Premium', '2025-04-15', '2025-06-25 10:20:00'),
        (104, 'Adi Iyer', 'adi.iyer@corp.com', 'Chennai', 'Tamil', 'Cancelled', '2024-11-05', '2025-06-25 10:30:00'),
        (105, 'Mahesh Chauhan', 'mahesh@zee.com', 'Lucknow', 'Urdu', 'Free', '2025-05-05', '2025-06-25 10:40:00'),
        (106, 'Sandeep Panigrahi', 'sandeep@orissa.net', 'Bhubaneswar', 'Odia', 'Premium', '2025-02-20', '2025-06-25 10:50:00'),
        (107, 'Jaanu Kumari', 'jaanu.kumari@indmail.com', 'Patna', 'Bhojpuri', 'Free', '2025-06-01', '2025-06-25 11:00:00'),
        (108, 'Chirkut Sharma', 'chirkut@funny.co.in', 'Agra', 'Hindi', 'Cancelled', '2024-10-20', '2025-06-25 11:10:00')
    ]

    df=pd.DataFrame(data,columns=[
        'customer_id', 'full_name', 'email_address', 'current_city',
        'preferred_language', 'subscription_status',
        'last_purchase_date', 'last_updated'
    ])

    with engine.begin() as con:
        con.execute(text(create_stmt))
        df.to_sql('customer_dim',index=False,con=con,if_exists='replace')
    
    print("Sample table created")


def insert_new_customer_data():
    engine = get_mysql_engine()

    new_data = pd.DataFrame([
        # New customer (changed ID to avoid conflict)
        {
            'customer_id': 109,
            'full_name': 'Smruthi Roy',
            'email_address': 'smruthi@new.com',
            'current_city': 'Chennai',
            'preferred_language': 'Tamil',
            'subscription_status': 'Active',
            'last_purchase_date': '2025-06-25',
            'last_updated': pd.Timestamp('2025-06-26 14:00:00')
        },
        # Existing customer update
        {
            'customer_id': 101,
            'full_name': 'Tanuj Kasula',
            'email_address': 'tanuj_new@corp.com',
            'current_city': 'Bangalore',  # Changed from Hyderabad
            'preferred_language': 'Hindi',
            'subscription_status': 'Active',
            'last_purchase_date': '2025-06-26',
            'last_updated': pd.Timestamp('2025-06-26 15:30:00')
        }
    ])

    new_data.to_sql('customer_dim', con=engine, if_exists='append', index=False)
    print("✅ New and updated customer records inserted into MySQL source.")



if __name__=="__main__":
    insert_new_customer_data()
    # insert_sample_data()