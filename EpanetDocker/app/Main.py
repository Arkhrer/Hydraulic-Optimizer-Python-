import socket
from ObjectiveFunction import ObjectiveFunction
import os
import time
import gc
import io, sys

def TCPclient(host, port, msg):
    while True:
        try:
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_client.connect((host, port))
            break
        except socket.error:
            # print("Falha na conexão. Reconectando")
            pass
            
    bin_msg = bytearray(msg, "utf8")
    status = tcp_client.send(bin_msg)

    if status > 0:
        data = tcp_client.recv(1024)
        # print("Recieved", repr(data))

    tcp_client.close()

    del tcp_client
    del data
    del status
    del bin_msg

    gc.collect()



def UDPserver(host, port):
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    udp_server.bind(server_address)

    data = b""
    
    while data != b"Exit":
        data, address = udp_server.recvfrom(1024)
        if not data:
            break
        # print(str(data)[2:-1])
        # print(address)
        udp_server.sendto(data, address)
        if data != b"Exit":

            #keep a named handle on the prior stdout 
            old_stdout = sys.stdout 
            #keep a named handle on io.StringIO() buffer 
            new_stdout = io.StringIO() 
            #Redirect python stdout into the builtin io.StringIO() buffer 
            sys.stdout = new_stdout 

            exec(f"ObjectiveFunction({str(data)[2:-1].split(',')})")

            result = sys.stdout.getvalue().strip()

            sys.stdout = old_stdout 

            TCPclient("127.0.0.1", port + 500, result)

        # udp_server.sendto(data, address)

    udp_server.close()

    del udp_server
    del server_address
    del data
    del address

    gc.collect()

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    # print(port)
    UDPserver("127.0.0.1", port)