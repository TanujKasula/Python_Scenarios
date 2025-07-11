from src.gmail_extract import extract_unread_emails_data
import pprint

if __name__=="__main__":
    data=extract_unread_emails_data()
    pprint.pprint(data)