import socket
from sys import argv
from typing import Optional
import os 
from threading import Thread

def http_response(code, explanation_str, body: Optional[bytes]=None):
    header = f"HTTP/1.1 {code} {explanation_str}\r\n"
    if body is not None:
        header += f"Content-Length: {len(body)}\r\n"
    header += "\r\n"
    response = header.encode(encoding='ascii')
    if body is not None:
        response += body
    return response

class Http_exception(Exception):
    def __init__(self, code, explanation_str):
        self.code = code
        self.explanation_str = explanation_str

    def transfer_to_request(self):
        return http_response(self.code, self.explanation_str, f"{self.code} {self.explanation_str}".encode(encoding='ascii'))
    
    @classmethod
    def error_400(cls):
        return cls(400, "Bad Request")

    @classmethod
    def error_404(cls):
        return cls(404, "Not Found")


class Server:
    def __init__(self, port):
        self._port = port

    def start(self):
        client_number = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind(('localhost', self._port))
            server_sock.listen()
            print('server is on')
            while True:
                conn, addr = server_sock.accept()
                Thread(target=self.handle_new_client, args=(conn,)).start()
                client_number += 1
                print(f"client number {client_number} has connected to the server")


    def handle_new_client(self, client_socket):
        with client_socket:
            try:
                file_request_path = self.handle_GET(client_socket)
                file = self.find_file(file_request_path)
                client_socket.sendall(http_response(200, "OK", file))
                print(f"File {file_request_path} sent successfully")                       
            except Http_exception as http_error:
                client_socket.sendall(http_error.transfer_to_request())        


    def handle_GET(self, conn):
        with conn.makefile('r') as http_request:
            fst_line = http_request.readline().split()
            if len(fst_line) != 3 or fst_line[0] != 'GET':
                raise Http_exception.error_400()
            path = fst_line[1]
            if path[0] == '/':
                path = path[1:]
            return path

    def find_file(self, path):
        if not os.path.isfile(path):
            raise Http_exception.error_404()
        with open(path, "rb") as f:
            return f.read()
def main():
    if len(argv) != 2:
        print(f"expected one argument, but received {len(argv) - 1}")
        exit(1)
    port = int(argv[1])
    if port < 1024 or port > 65535:
        print(f"invalid port")
        exit(1)
    server = Server(port)
    server.start()

if __name__ == "__main__":
    main()