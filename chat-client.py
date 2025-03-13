import socket
import threading

host = "localhost"
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))


def handle_server_data():
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(f"{data.decode()}")


th = threading.Thread(target=handle_server_data)
th.start()

while True:
    message = input("Enter your message: ")
    sock.send(message.encode())

th.join()
sock.close()