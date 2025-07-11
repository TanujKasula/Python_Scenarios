from src.util import get_sql_server_engine
from sqlalchemy import text

def insert_email_data(email_metadata,folder_url,email_text_url,attachment_urls):
    engine=get_sql_server_engine()

    with engine.begin() as conn:

        insert_comm_query=text("""
                                insert into gmail.Email_communications(
                                    sender_name, sender_email, receiver_name, receiver_email,
                                    cc, subject, body, email_date, folder_url, email_text_url
                                )
                               values(
                               :sender_name, :sender_email, :receiver_name, :receiver_email,
                                :cc, :subject, :body, :email_date, :folder_url, :email_text_url
                               );
                            """)
        # print("DEBUG:", email_metadata.keys())
        conn.execute(insert_comm_query,{
            "sender_name":email_metadata.get("sender_name"),
            "sender_email":email_metadata.get("sender_email"),
            "receiver_name":email_metadata.get("receiver_name"),
            "receiver_email": email_metadata.get("receiver_email"),
            "cc":email_metadata.get("cc"),
            "subject":email_metadata.get("subject"),
            "body":email_metadata.get("body"),
            "email_date":email_metadata.get("email_date"),
            "folder_url":folder_url,
            "email_text_url":email_text_url
        })

        if attachment_urls:
            insert_attachments_query=text("""
                                        insert into gmail.email_attachments(folder_url,sender_email,attachment_url)
                                          values(:folder_url,:sender_email,:attachment_url);
                                        """)
            for attachment_url in attachment_urls:
                conn.execute(insert_attachments_query,{
                    "folder_url":folder_url,
                    "sender_email":email_metadata.get("sender_email"),
                    "attachment_url":attachment_url
                })

        flat_insert_query=text("""
                                    insert into gmail.Email_Communications_Flat (
                                        sender_name, sender_email, receiver_name, receiver_email,
                                        cc, subject, body, email_date,email_text_url,
                                        attachment_1_url, attachment_2_url, attachment_3_url, attachment_4_url
                                    )values (
                                        :sender_name, :sender_email, :receiver_name, :receiver_email,
                                        :cc, :subject, :body, :email_date,:email_text_url,
                                        :a1, :a2, :a3, :a4
                                    );                                
                                """)
        conn.execute(flat_insert_query, {
            "sender_name": email_metadata.get("sender_name"),
            "sender_email": email_metadata.get("sender_email"),
            "receiver_name": email_metadata.get("receiver_name"),
            "receiver_email": email_metadata.get("receiver_email"),
            "cc": email_metadata.get("cc"),
            "subject": email_metadata.get("subject"),
            "body": email_metadata.get("body"),
            "email_date": email_metadata.get("email_date"),
            "email_text_url":email_text_url,
            "a1": attachment_urls[0] if len(attachment_urls)>0 else None,
            "a2": attachment_urls[1] if len(attachment_urls)>1 else None,
            "a3": attachment_urls[2] if len(attachment_urls)>2 else None,
            "a4": attachment_urls[3] if len(attachment_urls)>3 else None
        })
        print("All the data is inserted into the successfully")