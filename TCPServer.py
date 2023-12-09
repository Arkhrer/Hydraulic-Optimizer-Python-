import socket

def TCPserver(host, port):
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((host, port))

    tcp_server.listen()
    conn, addr = tcp_server.accept()
    result = ""

    while 1:
        data = conn.recv(1024)
        if not data:
            break

        result = data.decode("utf-8")
        # print("Recieved result ", result)
        
        conn.sendall(data)

    conn.close()

    return result

if __name__ == '__main__':
    TCPserver("localhost", 9001)