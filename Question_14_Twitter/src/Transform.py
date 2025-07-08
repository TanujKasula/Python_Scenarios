import os
import html
import re
import pandas as pd


def clean_text(text):
    text=html.unescape(text)
    text=re.sub(r"http\S+","",text)
    text=re.sub(r"@\w+","",text)
    text=re.sub(r"#\w+","",text)
    text=re.sub(r"[^\w\s.,!?]","",text)
    text=re.sub(r"\s+"," ",text)
    return text.strip().lower()

def clean_csv(file_name):
    base_path=os.path.dirname(os.path.dirname(__file__))
    data_dir=os.path.join(base_path,"data")
    file_path=os.path.join(data_dir,file_name)

    if not os.path.exists(file_path):
        print(f"File not found at :{file_path}")
        return None
    df=pd.read_csv(file_path)

    if "text" not in df.columns:
        print("Missing text column in csv.")
        return None
    
    df['cleaned_text']=df['text'].astype(str).apply(clean_text)

    df['created_at']=pd.to_datetime(df["created_at"]).dt.date

    output_file_path=file_path.replace(".csv","_cleaned.csv")
    df.to_csv(output_file_path,index=False)
    print("Cleaned the input file")
    return output_file_path

if __name__=="__main__":
    path=clean_csv("iphone_15.csv")
    print(path)