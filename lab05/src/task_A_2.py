import socket
import base64
import ssl
import sys

mail_pass = ''

def send(sender, addresser, subject, message, message_type='text/plain'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smtp_server = 'smtp.mail.ru'
    port = 587
    client_socket.connect((smtp_server, port))
    response = client_socket.recv(1024)
    print(response.decode())

    client_socket.sendall(b'EHLO example.com\r\n')
    response = client_socket.recv(1024)
    print(response.decode())

    client_socket.sendall(b'STARTTLS\r\n')
    response = client_socket.recv(1024)
    print(response.decode())

    context = ssl.create_default_context()
    with context.wrap_socket(client_socket, server_hostname=smtp_server) as ssl_socket:
        ssl_socket.write(b'EHLO example.com\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())
        
        ssl_socket.sendall(b'AUTH LOGIN\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(base64.b64encode(sender.encode()) + b'\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(base64.b64encode(mail_pass.encode()) + b'\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(f'MAIL FROM: <{sender}>\r\n'.encode())
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(f'RCPT TO: <{addresser}>\r\n'.encode())
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(b'DATA\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

        message = f'From: {sender}\r\nTo: {addresser}\r\nSubject: {subject}\r\nContent-Type: {message_type}; charset="utf-8"\r\n\r\n{message}'
        ssl_socket.sendall(message.encode())
        ssl_socket.sendall(b'\r\n.\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

        ssl_socket.sendall(b'QUIT\r\n')
        response = ssl_socket.recv(1024)
        print(response.decode())

    client_socket.close()
    print('mail was sent')

if __name__ == "__main__":
    if len(sys.argv[1:]) != 2:
        print(f"i see {len(sys.argv[1:])} args, 2 expected (addresser, mail_pass)")
        sys.exit(1)

    sender = 'iliabondarenko02@mail.ru' 
    addresser = sys.argv[1]
    mail_pass = sys.argv[2]  

    subject = 'test'
    message_txt = 'example of text 2 (txt)'
    message_html = '<h1>Hi</h1><p>this is sample message 2 (HTML)</p>'

    send(sender, addresser, subject, message_txt, 'text/plain')
    send(sender, addresser, subject, message_html, 'text/html')
