import sys, socket

def request_format(path):
    return f"GET /{path} HTTP/1.1\r\n".encode(encoding='ascii')

def http_client():
    if len(sys.argv) != 4:
        print("Usage: python3 <client.exe> server_host server_port filename")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    client_socket = socket.socket()
    client_socket.connect((server_host, server_port))
    query = request_format(filename)
    client_socket.sendall(query)
    response = b''
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part
    print(response.decode('utf-8'))


if __name__ == "__main__":
    http_client()
