import pandas as pd
from sqlalchemy import create_engine
from src.utils import get_config
import urllib

def load_data(df):
    config=get_config()
    mysql=config['MYSQL']
    #i encoded the password as the password contains spwcial characters like @#$%^& 
    encoded_password = urllib.parse.quote_plus(mysql['password'])
    connection_str=f"mysql+mysqlconnector://{mysql['user']}:{encoded_password}@{mysql['host']}:{mysql['port']}/{mysql['database']}"
    engine=create_engine(connection_str)

    df.to_sql(name='customers',index=False,con=engine,if_exists='replace')