import socket
import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 12345)
client_socket.settimeout(1.0)  

for i in range(1, 11):
    message = f'Ping {i} {datetime.datetime.now()}'
    start_time = datetime.datetime.now() 
    client_socket.sendto(message.encode(), server_address)

    try:
        response, addr = client_socket.recvfrom(1024)
        end_time = datetime.datetime.now()  
        rtt = (end_time - start_time).total_seconds()  

        rtt_time = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        
      
        print(f'Ping {i} {rtt_time}, RTT: {rtt:.6f} seconds')

    except socket.timeout:
     
        print(f'Ping {i} Request timed out')

client_socket.close() 
