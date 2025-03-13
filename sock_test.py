import socket

host = "test.net"
port = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send(b"GET / HTTP/1.1\r\nHost: test.net\r\n\r\n")

data = sock.recv(1024)
print(data)

sock.close()
