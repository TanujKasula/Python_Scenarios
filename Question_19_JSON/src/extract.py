from src.util import get_sharepoint_context
from src.config import sharepoint_files
import io
import json
import pandas as pd

def extract_all_json_files():
    context,folder_url=get_sharepoint_context()
    dfs={}

    for name,filename in sharepoint_files.items():
        file_response = io.BytesIO()
        context.web.get_file_by_server_relative_url(f"{folder_url}/{filename}").download(file_response).execute_query()
        file_response.seek(0)  # Go to beginning of buffer
        json_data = json.load(file_response)

        df=pd.DataFrame(json_data)
        dfs[name]=df
    return dfs

