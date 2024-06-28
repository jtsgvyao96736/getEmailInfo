import imaplib
import email
from email.header import decode_header
email_user = "youEailAccount"
email_pass = "youEmailPwd"
imap_server = "your email imap"

mail = imaplib.IMAP4_SSL(imap_server)

mail.login(email_user, email_pass)

mail.select("inbox")

_, data = mail.search(None, "ALL")
mail_ids = data[0].split()

for id in mail_ids:
    _, msg_data = mail.fetch(id, "(RFC822)")
    raw_email = msg_data[0][1]

    msg = email.message_from_bytes(raw_email)

    from_ = decode_header(msg.get("From"))[0][0]
    subject = decode_header(msg.get("Subject"))[0][0]

    print(f"From: {from_}")
    print(f"Subject: {subject}")

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == "text/plain" and "attachment" not in cdispo:
                body = part.get_payload(decode=True).decode()
                print("Body:")
                print(body)
                break
    else:
        body = msg.get_payload(decode=True).decode()
        print("Body:")
        print(body)
        print('\n\n')

mail.logout()
