import socket

HOST = '0.0.0.0'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
    sock.listen(1)
except:
    print("Error binding to port")
    exit(1)

while True:
    conn, addr = sock.accept()
    print("Connected by", addr)
    data = conn.recv(1024)
    print(data)

    answer_data = ("HTTP/1.1 200 OK\r\nContent-Type: text/html; "
                   "charset=utf-8\r\nContent-Length: 5\r\n\r\nHello")

    conn.sendall(answer_data.encode())
    conn.close()