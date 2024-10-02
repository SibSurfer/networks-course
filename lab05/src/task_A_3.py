import socket
import base64
import ssl
import sys

mail_pass=''

def send(sender, addresser, subject, body, message_type, image_filename = '/home/ilia/Documents/networks-course/lab05/img/robot.jpg'):
    with open(image_filename, 'rb') as image_file:
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smtp_server = 'smtp.mail.ru'
    port = 587
    client_socket.connect((smtp_server, port))
    response = client_socket.recv(1024)
    print(response.decode())

    username = sender.split('@', maxsplit=1)[0]

    client_socket.sendall(f'EHLO {username}\r\n'.encode())
    response = client_socket.recv(1024)
    print(response.decode())

    client_socket.sendall(b"STARTTLS\r\n")
    response = client_socket.recv(1024)
    print(response.decode())

    with ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_SSLv23) as ssl_socket:
        ssl_socket.write(b"EHLO example.com\r\n")
        response = ssl_socket.read(1024)
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

        message = f'From: {sender}\r\nTo: {addresser}\r\nSubject: {subject}\r\n'
        message += f'Content-Type: multipart/mixed; boundary="boundary"\r\n\r\n'
        message += f'--boundary\r\n'
        message += f'Content-Type: {message_type}\r\n\r\n{body}\r\n\r\n'
        message += f'--boundary\r\n'
        message += f'Content-Type: image/jpeg\r\nContent-Transfer-Encoding: base64\r\n'
        message += f'Content-Disposition: attachment; filename="{image_filename}"\r\n\r\n'
        message += encoded_image + '\r\n'
        message += f'--boundary--\r\n'

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
    if (len(sys.argv[1:]) != 2):
        print(f"i see {len(sys.argv[1:])} args, 2 expected (addresser, mail_pass)")
        sys.exit(1)

    sender = 'iliabondarenko02@mail.ru'
    addresser = sys.argv[1]
    mail_pass = sys.argv[2] 
    subject = '3d task A'
    message_txt = 'example of text 3 (txt)'
    message_html = '<h1>Hi</h1><p>this is sample message 3 (HTML)</p>'

    send(sender, addresser, subject, message_txt, 'text/plain')
    send(sender, addresser, subject, message_html, 'text/html')