from src.gmail_extract import extract_unread_emails_data
from src.s3_uploader import upload_gmail_data
from src.db_insert import insert_email_data
from src.tables import create_tables

def main():
    print("STARTING PIPELINE.......")

    emails_data=extract_unread_emails_data()

    if not emails_data:
        print("No unread emails found")
        return

    for email in emails_data:
        print(f"Processing email from {email['sender_email']}......")

        email_metadata=email
        attachments=email.get('attachments',[])
        body=email.get('body',"")

        upload_result=upload_gmail_data(attachments,email_metadata,body)

        folder_url=upload_result['folder_url']
        email_text_url=upload_result['email_text_url']
        attachment_urls=upload_result['attachment_urls']

        create_tables()
        
        insert_email_data(email_metadata,folder_url,email_text_url,attachment_urls)


        print(f"Finished processing email from {email['sender_email']}\n")

if __name__=="__main__":
    main()