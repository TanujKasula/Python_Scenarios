import io
import pandas as pd
from src.util import get_sharepoint_context
from config import config

def extract():
    context=get_sharepoint_context()
    relative_path=f"/sites/kasmo-training/{config.document_library}/{config.sharepoint_folder}/{config.filename}"

    print("Extracting Data from Sharepoint")

    file=context.web.get_file_by_server_relative_url(relative_path)
    buffer=io.BytesIO()
    file.download(buffer).execute_query()
    buffer.seek(0)
    df=pd.read_excel(buffer)
    return df

if __name__=="__main__":
    df=extract()
    print(df)