from src.gmail_utils import get_credentials,authenticate_gmail
from src.gmail_reader import get_unread_mails,extract_email_details
import pprint

def mark_as_read(service,msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds':['UNREAD']}
    ).execute()

def extract_unread_emails_data():
    service=authenticate_gmail()

    msgs=get_unread_mails(service,max_results=1)
    emails_data=[]

    if not msgs:
        print("No unread messages found")
        return 
    
    for msg in msgs:
        msg_id=msg['id']
        email_data=extract_email_details(service,msg_id)
        emails_data.append(email_data)
        mark_as_read(service,msg_id)
        print(f"marked message {msg_id} as read.\n")

    return emails_data

if __name__=="__main__":
    data=extract_unread_emails_data()
    pprint.pprint(data)