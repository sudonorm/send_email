import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from typing import List

class EmailSender:
    
    def __init__(self):
        pass
    
    def send_email(self, *, messagePlainText: str, addHtml: bool = False, messageHtml: str = "", smtp_server: str, port: int, 
                   sender_email: str, password: str, receiver_emails: List = [], addAttachment: bool = False, 
                   attachmentFileName: str = "test.csv"):

        '''
            This function can be used to send an email via smtp. 
            
            It also allows for the addition of attachments; currently just pdfs and csvs have been tested to work. 
            
            It is set up to automatically bcc the sender a copy of the email, but this can be changed.
            
            Adapted from: https://realpython.com/python-send-email/
        '''
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)
        message["Bcc"] = sender_email

        # Turn this into plain MIMEText objects
        part1 = MIMEText(messagePlainText, "plain")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        if addHtml:
            if not messageHtml == "":
                # Turn this into html MIMEText objects
                part2 = MIMEText(messageHtml, "html")
                message.attach(part2)

        if addAttachment:
            filename = attachmentFileName  # Must be in same directory as script

            # Open file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message
            message.attach(part)

        # Convert message to string
        messageText = message.as_string()

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_emails, messageText
            )