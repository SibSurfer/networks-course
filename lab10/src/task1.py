import socket
import struct
import time
import sys

def checksum(data):
    if len(data) % 2:
        data += b'\x00'
    res = sum(struct.unpack('!H', data[i:i+2])[0] for i in range(0, len(data), 2))
    while res >> 16:
        res = (res & 0xFFFF) + (res >> 16)
    return ~res & 0xFFFF

def ping(host, count=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    
    ID = 12345
    seq_num = 1
    dest_addr = socket.gethostbyname(host)
    
    for i in range(count):
        header = struct.pack('!BBHHH', 8, 0, 0, ID, seq_num)
        data = struct.pack('d', time.time())
        checksum_val = checksum(header + data)
        header = struct.pack('!BBHHH', 8, 0, checksum_val, ID, seq_num)
        packet = header + data
        
        sock.sendto(packet, (host, 0))
        
        sock.settimeout(1) 
        
        try:
            start_time = time.time()
            data, addr = sock.recvfrom(1024)  
            end_time = time.time()
            
            rtt = (end_time - start_time) * 1000

            print(f'Ping {host} RTT={rtt:.1f} ms')  

        except socket.timeout:
            print(f'Request timeout for icmp_seq {i}') 
            continue
        
        seq_num += 1
        time.sleep(1)

    sock.close() 

if __name__ == '__main__':
    if (len(sys.argv[1:]) < 1):
        print(f"you provide {len(sys.argv[1:])} arguments, 1 expected (target_host)")
        sys.exit(1)

    target_host = sys.argv[1]
    ping(target_host, count=10)
