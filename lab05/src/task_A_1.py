import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

password = ''

def send(sender_email, receiver_email, subject, message, message_type='txt'):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    if message_type == 'txt':
        msg.attach(MIMEText(message, 'plain'))
    elif message_type == 'html':
        msg.attach(MIMEText(message, 'html'))

    with smtplib.SMTP('smtp.mail.ru', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

if __name__ == "__main__":
    if (len(sys.argv[1:]) != 2):
        print(f"been provided {len(sys.argv[1:])} args, but 2 args expected (receiver_email, sender_password)")
        sys.exit(1)

    sender_email = 'iliabondarenko02@mail.ru'
    receiver_email = sys.argv[1]
    password = sys.argv[2] 
    subject = 'testing mail'
    message_txt = 'example of text (txt)'
    message_html = '<h1>Hi</h1><p>this is sample message (HTML)</p>'

    send(sender_email, receiver_email, subject, message_txt, 'txt')
    send(sender_email, receiver_email, subject, message_html, 'html')