import socket

def UDPclient(host, port, msg):
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address=(host, port)

    bin_msg = bytearray(msg, "utf8")
    status = udp_client.sendto(bin_msg, server_address)
    # status = udp_client.sendto(b'Exit', server_address)

    if status > 0:
        data = udp_client.recvfrom(1024)
        # print("Received", repr(data))

    udp_client.close()


if __name__ == '__main__':
    UDPclient("localhost", 9001, "Exit")