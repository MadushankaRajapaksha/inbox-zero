import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def decode_header_value(value):
    if value is None:
        return ""
    decoded, enc = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(enc or "utf-8", errors="ignore")
    return decoded


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(
                        "utf-8", errors="ignore"
                    )
                except:
                    continue
    else:
        if msg.get_content_type() == "text/plain":
            return msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    return ""


# Connect to Gmail IMAP
imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login(EMAIL, APP_PASSWORD)

# Select INBOX
imap.select("INBOX")

status, messages = imap.search(None, "ALL")
email_ids = messages[0].split()

# Get last email
latest = email_ids[-1]

status, msg_data = imap.fetch(latest, "(RFC822)")
raw_msg = msg_data[0][1]
msg = email.message_from_bytes(raw_msg)

# Map values
mapped_email = {
    "id": int(latest.decode()),  # message ID
    "from": decode_header_value(msg.get("From")),
    "to": decode_header_value(msg.get("To")),
    "subject": decode_header_value(msg.get("Subject")),
    "date": decode_header_value(msg.get("Date")),
    "body": get_email_body(msg),
    "unread": "UNSEEN" in imap.fetch(latest, "(FLAGS)")[1][0].decode(),
}

import json

with open("email.json", "w") as f:
    json.dump(mapped_email, f, indent=4)

imap.close()
imap.logout()

# import os
# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv

# load_dotenv()

# EMAIL = os.getenv("EMAIL")
# APP_PASSWORD = os.getenv("APP_PASSWORD")

# msg = MIMEText("Hello! This is a test email from Python.")
# msg["Subject"] = "Python SMTP Test"
# msg["From"] = EMAIL
# msg["To"] = "000x@purelymail.com"

# # Connect to Gmail SMTP
# with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#     smtp.login(EMAIL, APP_PASSWORD)
#     smtp.send_message(msg)

# print("Email Sent!")
