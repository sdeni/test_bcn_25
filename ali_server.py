import socket

HOST = '0.0.0.0'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
    sock.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
except:
    print('Error binding to port')
    exit(1)

conn, addr = sock.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Client received {data.decode()}")


    # answer_data = ("HTTP/1.1 200 OK\nContent-Type: text/html;"
    #                 "charset=utf-8\r\nContent-Length: 5\r\n\r\nHello")

    message = input("Enter your message: ")
    conn.send(message.encode())

conn.close()
sock.close()


