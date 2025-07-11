from src.gmail_utils import authenticate_gmail
from email import message_from_bytes
import base64
from email.header import decode_header, make_header
import re
from datetime import datetime
from email.utils import parsedate_to_datetime


def parse_name_email(raw):
    pattern_match=re.match(r'(.*)<(.*)>',raw)
    if pattern_match:
        return pattern_match.group(1).strip().strip('"'), pattern_match.group(2).strip()
    return "",raw.strip()

def get_unread_mails(service,max_results=2):
    result=service.users().messages().list(
        userId='me',
        labelIds=['UNREAD'],
        maxResults=max_results
    ).execute()
    return result.get('messages',[])

def extract_email_details(service,msg_id):
    msg=service.users().messages().get(userId='me',id=msg_id,format='raw').execute()
    raw=base64.urlsafe_b64decode(msg['raw'].encode('utf-8'))
    mime_msg=message_from_bytes(raw)

    sender_name,sender_email=parse_name_email(mime_msg.get('From',''))
    receiver_name,receiver_email=parse_name_email(mime_msg.get('To',''))
    cc=mime_msg.get('Cc','')
    subject=str(make_header(decode_header(mime_msg.get('Subject',''))))
    raw_date = mime_msg.get('Date','')
    try:
        email_date = parsedate_to_datetime(raw_date)
    except Exception as e:
        print(f"Warning: Failed to parse email_date '{raw_date}'. Error: {e}")
        email_date = None

    body_parts = []
    attachments=[]

    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type=part.get_content_type()
            content_disposition=str(part.get("Content-Disposition",""))
            
            if content_type=="text/plain" and "attachment" not in content_disposition:
                try:
                    body_parts.append(part.get_payload(decode=True).decode())
                except:
                    pass
            elif "attachment" in content_disposition:
                filename=part.get_filename()
                if filename:
                    try:
                        file_data=part.get_payload(decode=True)
                        attachments.append({
                            "filename":filename,
                            "file_data":file_data
                        })
                    except Exception as e:
                        print(f"Error decoding {filename}:{e}")
    else:
        try:
            body=mime_msg.get_payload(decode=True).decode()
        except:
            pass
    body = "\n".join(body_parts)

    return {
        "sender_name":sender_name,
        "sender_email":sender_email,
        "receiver_name":receiver_name,
        "receiver_email":receiver_email,
        "cc":cc,
        "subject":subject,
        "email_date":email_date,
        "body":body,
        "attachments":attachments
    }