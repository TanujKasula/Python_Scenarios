import os
import tweepy
import pandas as pd
from dotenv import load_dotenv
import re

import tweepy.client

load_dotenv()

bearer_token=os.getenv("x_bearer")

client=tweepy.Client(bearer_token)

def clean_query(query):
    return re.sub(r"\W+","_",query.strip()).lower()

def fetch_tweets(query,max_results=2):
    search_query=f"{query} -is:retweet lang:en"
    response=client.search_recent_tweets(
        query=search_query,
        tweet_fields=["created_at","lang"],
        max_results=max_results
    )

    if not response.data:
        print(f"No tweets found for the query :{query}")
        return pd.DataFrame()
    
    tweets=[]
    for tweet in response.data:
        tweets.append({
            "text":tweet.text,
            "created_at":tweet.created_at,
            "lang":tweet.lang
        })
    
    df=pd.DataFrame(tweets)

    filename=clean_query(query)+".csv"
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)

    file_path=os.path.join(data_dir,filename)
    df.to_csv(file_path,index=False)
    print(f"File saved to :{file_path}")

    return file_path

if __name__=="__main__":
    file_path = fetch_tweets("Celestial", max_results=3)
    print(f"CSV is saved at: {file_path}")
